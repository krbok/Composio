"""Proves the research pipeline on 5 deliberately different apps before
scaling to the full 100. See /Users/kritik/.claude/plans/sequential-dazzling-sonnet.md
for why each app is in this set.

Usage: python -m research.stress_test
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv

from research.agent import AgentDidNotSubmitError, research_app

STRESS_TEST_APPS = [
    # (app, category, hint, why it's here)
    ("Stripe", "Finance and Fintech", "stripe.com/docs/api",
     "clean docs, API key, self-serve -- the easy case"),
    ("Salesforce", "CRM and Sales", "salesforce.com",
     "OAuth2, huge doc surface -- tests extraction at scale"),
    ("Amazon Selling Partner", "Ecommerce", "developer-docs.amazon.com/sp-api",
     "partner-gated -- must report gated, not hallucinate a self-serve path"),
    ("fanbasis", "Ecommerce", "fanbasis.com",
     "obscure, thin docs -- low confidence MUST fire here"),
    ("Otter AI", "AI, Research and Media-native", "help.otter.ai (MCP server)",
     "tests has_mcp = yes-official detection"),
]

OUT_PATH = Path(__file__).resolve().parent.parent / "out" / "stress_test.json"


async def main() -> None:
    load_dotenv()
    rows: list[dict] = []
    failures: list[str] = []

    for app, category, hint, why in STRESS_TEST_APPS:
        print(f"\n=== {app} ({why}) ===")
        try:
            finding = await research_app(app, category, hint)
        except AgentDidNotSubmitError as exc:
            print(f"FAILED: {exc}")
            failures.append(app)
            continue

        row = finding.model_dump(mode="json")
        rows.append(row)
        print(json.dumps(row, indent=2))

    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(json.dumps(rows, indent=2))
    print(f"\nWrote {len(rows)}/{len(STRESS_TEST_APPS)} rows to {OUT_PATH}")
    if failures:
        print(f"Apps the agent could not complete: {failures}")


if __name__ == "__main__":
    asyncio.run(main())
