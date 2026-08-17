"""Research agents.

Two independent ways to research the same app, sharing one turn-loop
(`_run_agent_turn`) and one output contract (`submit_finding`, whose input
schema is generated straight from `AgentSubmission` -- so the enum/URL/
confidence constraints are part of the tool-call contract, not a hope that
the model emits well-formed freeform JSON):

- `research_app()` -- the primary pass. Web search + page fetch via
  Composio's COMPOSIO_SEARCH_WEB / COMPOSIO_SEARCH_FETCH_URL_CONTENT (both
  free and NO_AUTH, Exa-backed).
- `research_app_second_pass()` -- the Stage-2 verification pass. Claude's
  native WebSearch/WebFetch instead of Composio's tools -- a differently
  implemented search+fetch stack, not just a repeated call, so it's a
  meaningful second signal rather than re-asking the same question the same
  way twice (see research/verify.py). This was originally meant to use
  Composio's BROWSER_TOOL for an even more distinct mechanism (real cloud
  browser automation), but that toolkit is disabled at the account/org
  level on this Composio key.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    ToolUseBlock,
    create_sdk_mcp_server,
    tool,
)
from composio import Composio
from composio_claude_agent_sdk import ClaudeAgentSDKProvider

from research.schema import AgentSubmission, Finding

USER_ID = "app-research"

# claude-agent-sdk shells out to the `claude` CLI by default. We install it
# as a local (not global) npm dependency so the repo is reproducible with
# just `npm install` -- no assumptions about what's on the runner's PATH.
_LOCAL_CLI_PATH = Path(__file__).resolve().parent.parent / "node_modules" / ".bin" / "claude"

SEARCH_TOOL_SLUGS = ["COMPOSIO_SEARCH_WEB", "COMPOSIO_SEARCH_FETCH_URL_CONTENT"]

# Shared across both passes so the two signals disagree because of what they
# *found*, not because they were told to judge findings by different rules.
JUDGING_CRITERIA = """Rules:
- evidence_url MUST be a URL you actually visited/fetched this turn, never a \
guessed or remembered URL.
- If the app is gated behind a paid plan, partnership, or admin approval, \
say so plainly in self_serve_status and main_blocker -- that is a correct, \
valuable finding, not a failure. Do not round up to a friendlier tier to \
seem more optimistic about buildability.
- If docs are thin, contradictory, or you could not verify a claim, lower \
confidence accordingly instead of guessing to fill the field.
- has_mcp is commonly gotten wrong by skipping the check once auth/self-serve \
already look resolved. It is NOT optional: you MUST run one search or fetch \
specifically aimed at "<app> MCP server" / "<app> Model Context Protocol" \
before submitting, even if you are already confident about every other \
field. Only after that dedicated check may you conclude has_mcp = no. \
yes-official only if the app's own docs describe an MCP server they \
publish; yes-community if you find one but it's third-party; otherwise no.

Judging self_serve_status -- read this carefully, it is the field most \
often gotten wrong:

A Composio toolkit is MULTI-TENANT: many different end-users will each \
connect their OWN account through it. Always judge self_serve_status by \
what THAT requires, never by what a single developer needs for their own \
personal/internal access to their own account -- those are frequently \
different tiers with different requirements, and the personal-access tier \
is almost always the easier, wrong answer to report.

Concretely, many platforms offer two separate paths:
- a "private app" / personal-use path (register, request a role/scope for \
your own account, sometimes auto-approved or lightly reviewed), and
- a "public app" / ISV / marketplace-listed path (what you need so OTHER \
users can connect their own accounts through your integration) -- this is \
the one that determines a Composio toolkit's real gating, even when the \
private path looks easy.

Use these definitions in order from least to most restrictive, and pick \
based on the multi-tenant path specifically:
- self-serve-free: any developer can register and get working multi-tenant \
credentials (e.g. a public OAuth app) immediately, free, with no human \
review of the application itself.
- self-serve-trial: same, but time/usage-limited or requires payment info \
that converts to paid later -- the signup itself is still instant/no-review.
- paid-plan: the platform itself requires a specific paid subscription \
tier before multi-tenant API/developer access is available at all, but \
upgrading to unlock it is self-serve (no human review).
- admin-approval: a human at the platform (or the end-user's own org admin) \
reviews and approves your specific multi-tenant application/role before \
you get credentials, but no formal partnership or marketplace listing is \
required -- e.g. "submit a request, we'll email you API access."
- partner-gated: building a multi-tenant integration requires becoming a \
listed partner/ISV/solution-provider -- e.g. app marketplace review and \
approval, a partnership agreement, or a "contact sales" enterprise gate. \
If the ONLY way for other users to connect their accounts through your \
integration is to first get your integration approved/listed by the \
platform (as opposed to just approved for your own account), this is \
partner-gated, even if a separate private/personal-use path is easier.
"""

SEARCH_SYSTEM_PROMPT = f"""You are a research analyst who evaluates whether \
an app could become a Composio agent toolkit today.

For the app you are given:
1. Use web search to find the app's OFFICIAL developer/API documentation \
(not marketing pages, not third-party blog posts).
2. Fetch and actually read the auth/authentication page and the \
getting-started or quickstart page.
3. If the first page you land on is thin, ambiguous, or you are not sure \
it's the official docs, search again or fetch another page before \
concluding. Do not guess.
4. When you are confident (or have exhausted reasonable search effort), \
call submit_finding exactly once with your conclusions. That is your final \
action -- do not write a prose summary afterward.

{JUDGING_CRITERIA}"""

# Kept deliberately independent of SEARCH_SYSTEM_PROMPT: it is not told the
# first pass's answer, and it uses a different search+fetch implementation
# (Claude's native WebSearch/WebFetch, not Composio's Exa-backed tools), so
# it can't just rediscover the same mistake the same way -- it's a genuine
# second opinion, not a repeat.
#
# This was originally meant to use Composio's BROWSER_TOOL (a real cloud
# browser) as an even more distinct mechanism, but that toolkit is disabled
# at the account/org level on this Composio key ("temporarily disabled by
# the administrator") -- an infrastructure limit, not a bug here. Native
# WebSearch/WebFetch is the fallback: still an independently-implemented
# stack, just not literal browser automation.
SECOND_PASS_SYSTEM_PROMPT = f"""You are a research analyst independently \
verifying whether an app could become a Composio agent toolkit today. You \
have NOT seen any prior research on this app -- form your own conclusions \
from scratch.

For the app you are given:
1. Use WebSearch to find the app's OFFICIAL developer/API documentation \
(not marketing pages, not third-party blog posts).
2. Use WebFetch to actually read the auth/authentication page and the \
getting-started or quickstart page.
3. If the first page you land on is thin, ambiguous, or you are not sure \
it's the official docs, search again or fetch another page before \
concluding. Do not guess.
4. If a tool is unavailable or errors, say so and lower confidence \
accordingly -- never answer from general/parametric knowledge without \
having actually fetched a page this turn.
5. When you are confident (or have exhausted reasonable effort), call \
submit_finding exactly once with your conclusions. That is your final \
action -- do not write a prose summary afterward.

{JUDGING_CRITERIA}"""


def _submit_finding_description() -> str:
    return (
        "Submit the completed research finding for this app. Call this "
        "exactly once, as your final action, once you have read the app's "
        "official docs."
    )


def _build_submission_tool() -> tuple[Any, dict[str, Any]]:
    """Fresh tool + capture box per call, so concurrent/sequential runs
    never share state."""
    captured: dict[str, Any] = {}

    @tool(
        "submit_finding",
        _submit_finding_description(),
        AgentSubmission.model_json_schema(),
    )
    async def submit_finding(args: dict[str, Any]) -> dict[str, Any]:
        captured["value"] = args
        return {"content": [{"type": "text", "text": "Recorded."}]}

    return submit_finding, captured


_mcp_servers: dict[str, Any] = {}


def _get_mcp_server(name: str, tool_slugs: list[str]) -> Any:
    """Lazily build (once per name) an MCP server wrapping just the given
    tool slugs -- never Composio's full 1000+ toolkit catalog, so tool
    discovery stays fast and the model isn't tempted to reach for unrelated
    tools."""
    if name not in _mcp_servers:
        composio = Composio(provider=ClaudeAgentSDKProvider())
        composio_tools = composio.tools.get(user_id=USER_ID, tools=tool_slugs)
        _mcp_servers[name] = create_sdk_mcp_server(name=name, tools=composio_tools)
    return _mcp_servers[name]


class AgentDidNotSubmitError(RuntimeError):
    """Raised when the agent's turn ended without calling submit_finding --
    a hard failure for that row, never silently defaulted."""


async def _run_agent_turn(
    app: str,
    category: str,
    hint: str,
    system_prompt: str,
    mcp_server_name: str | None = None,
    tool_slugs: list[str] | None = None,
    built_in_tools: list[str] | None = None,
) -> Finding:
    if not os.environ.get("COMPOSIO_API_KEY"):
        raise RuntimeError("COMPOSIO_API_KEY is not set (check your .env)")

    # Drop ANTHROPIC_API_KEY from our own process env (if present) before
    # the CLI subprocess is spawned -- it inherits our env, and a metered
    # API key present there always wins over the CLI's own claude.ai login,
    # which is the free path (subscription-based, no per-token billing).
    os.environ.pop("ANTHROPIC_API_KEY", None)

    submit_tool, captured = _build_submission_tool()
    research_server = create_sdk_mcp_server(name="research", tools=[submit_tool])

    mcp_servers = {"research": research_server}
    if mcp_server_name and tool_slugs:
        mcp_servers[mcp_server_name] = _get_mcp_server(mcp_server_name, tool_slugs)

    options = ClaudeAgentOptions(
        system_prompt=system_prompt,
        mcp_servers=mcp_servers,
        permission_mode="bypassPermissions",
        cli_path=str(_LOCAL_CLI_PATH) if _LOCAL_CLI_PATH.exists() else None,
        max_turns=20,
        # Isolation: the subprocess otherwise inherits the full ambient
        # Claude Code environment (Bash, Edit, Write, Task, any globally
        # configured MCP servers, project/user settings). Combined with
        # bypassPermissions that's a real risk for an unattended batch loop,
        # so lock it down to exactly the tools explicitly passed in --
        # nothing else.
        tools=built_in_tools or [],
        strict_mcp_config=True,
        setting_sources=[],
    )

    tool_calls: list[str] = []

    async with ClaudeSDKClient(options=options) as client:
        await client.query(
            f"Research the app '{app}' (category: {category}). "
            f"Website / hint: {hint}."
        )
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, ToolUseBlock):
                        tool_calls.append(block.name)

    if "value" not in captured:
        raise AgentDidNotSubmitError(
            f"{app}: agent turn ended without calling submit_finding "
            f"(tool calls made: {tool_calls})"
        )

    submission = AgentSubmission.model_validate(captured["value"])
    return Finding(app=app, category=category, **submission.model_dump())


async def research_app(app: str, category: str, hint: str) -> Finding:
    return await _run_agent_turn(
        app, category, hint, SEARCH_SYSTEM_PROMPT, mcp_server_name="composio", tool_slugs=SEARCH_TOOL_SLUGS
    )


async def research_app_second_pass(app: str, category: str, hint: str) -> Finding:
    return await _run_agent_turn(
        app, category, hint, SECOND_PASS_SYSTEM_PROMPT, built_in_tools=["WebSearch", "WebFetch"]
    )
