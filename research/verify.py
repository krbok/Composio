"""Stage-2 verification: cross-check each Stage-1 Finding against two
independent signals before trusting it.

Signal A -- Composio's own catalog (composio.toolkits.get). Free, instant,
deterministic ground truth for auth_method on any app that already has a
Composio toolkit. Weak signal when the slug match is ambiguous (a generic
"amazon" toolkit entry isn't necessarily the Selling Partner API
specifically) -- flagged as such, not silently trusted.

Signal B -- a second, independent research pass using a differently
implemented search+fetch stack (Claude's native WebSearch/WebFetch, not
Composio's Exa-backed tools), re-deriving the finding from scratch without
seeing the first pass's answer (no anchoring). This is what catches
same-tool non-determinism: the 5-app stress test showed the search-based
agent flip has_mcp from correct to incorrect between two runs of the
identical tool -- a differently implemented tool disagreeing is a real
signal; two runs of the same tool agreeing with each other is not.

Policy: rows where both signals agree get bumped to high confidence and skip
human review. Rows where either signal disagrees (or first-pass confidence
was already low) are flagged for human review with the specific field-level
diff -- never silently overwritten.
"""

from __future__ import annotations

import re

from composio import Composio
from composio_client import NotFoundError
from pydantic import BaseModel, Field

from research.agent import research_app_second_pass
from research.schema import AuthMethod, Finding

LOW_CONFIDENCE_THRESHOLD = 0.75

COMPARED_FIELDS = [
    "auth_method",
    "self_serve_status",
    "api_surface",
    "api_breadth",
    "has_mcp",
    "buildability",
]

# Composio's catalog uses its own scheme names; map them onto our enum.
# Anything not listed here (e.g. custom/JWT variants) intentionally maps to
# OTHER rather than guessing, so a bad mapping can't manufacture a false
# agreement.
_SCHEME_TO_AUTH_METHOD = {
    "OAUTH2": AuthMethod.OAUTH2,
    "OAUTH1": AuthMethod.OAUTH2,
    "API_KEY": AuthMethod.API_KEY,
    "BASIC": AuthMethod.BASIC,
    "BASIC_WITH_JWT": AuthMethod.BASIC,
    "BEARER_TOKEN": AuthMethod.TOKEN,
}


def _slugify(app_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", app_name.lower()).strip("_")


class CatalogCheck(BaseModel):
    toolkit_slug: str
    found: bool
    catalog_schemes: list[str] = Field(default_factory=list)
    agrees: bool | None = None
    note: str = ""


class FieldDisagreement(BaseModel):
    field: str
    first_pass: str
    second_pass: str


class VerificationResult(BaseModel):
    app: str
    first_pass: Finding
    catalog_check: CatalogCheck
    second_pass: Finding
    disagreements: list[FieldDisagreement]
    needs_human_review: bool
    review_reason: str
    final_confidence: float


_composio_client: Composio | None = None


def _get_composio_client() -> Composio:
    global _composio_client
    if _composio_client is None:
        _composio_client = Composio()
    return _composio_client


def _extract_schemes(toolkit) -> list[str]:
    data = toolkit.model_dump()
    schemes: set[str] = set()
    for m in data.get("composio_managed_auth") or []:
        if m.get("mode"):
            schemes.add(m["mode"])
    deprecated = data.get("deprecated") or {}
    for r in deprecated.get("raw_proxy_info_by_auth_schemes") or []:
        if r.get("auth_method"):
            schemes.add(r["auth_method"])
    return sorted(schemes)


def catalog_cross_check(finding: Finding) -> CatalogCheck:
    slug = _slugify(finding.app)
    client = _get_composio_client()
    try:
        toolkit = client.toolkits.get(slug=slug)
    except NotFoundError:
        return CatalogCheck(toolkit_slug=slug, found=False, note="no Composio toolkit exists for this app")
    except Exception as exc:  # network/auth errors -- don't block the run on this
        return CatalogCheck(toolkit_slug=slug, found=False, note=f"lookup failed: {exc}")

    schemes = _extract_schemes(toolkit)
    if not schemes:
        return CatalogCheck(toolkit_slug=slug, found=True, note="toolkit found but declares no auth schemes")

    mapped = {_SCHEME_TO_AUTH_METHOD.get(s, AuthMethod.OTHER) for s in schemes}
    return CatalogCheck(
        toolkit_slug=slug,
        found=True,
        catalog_schemes=schemes,
        agrees=finding.auth_method in mapped,
        note="naive slug match -- may not be the exact same product" if slug in ("amazon",) else "",
    )


async def verify_finding(first_pass: Finding, hint: str) -> VerificationResult:
    catalog_check = catalog_cross_check(first_pass)
    second_pass = await research_app_second_pass(first_pass.app, first_pass.category, hint)

    disagreements = [
        FieldDisagreement(field=field, first_pass=str(getattr(first_pass, field)), second_pass=str(getattr(second_pass, field)))
        for field in COMPARED_FIELDS
        if getattr(first_pass, field) != getattr(second_pass, field)
    ]
    if catalog_check.agrees is False:
        disagreements.append(
            FieldDisagreement(
                field="auth_method (vs Composio catalog)",
                first_pass=str(first_pass.auth_method),
                second_pass=f"catalog declares {catalog_check.catalog_schemes}",
            )
        )

    reasons = []
    if disagreements:
        reasons.append(f"{len(disagreements)} field disagreement(s) with the independent browser-based pass")
    if first_pass.confidence < LOW_CONFIDENCE_THRESHOLD:
        reasons.append(f"first-pass confidence {first_pass.confidence} below {LOW_CONFIDENCE_THRESHOLD}")

    needs_human_review = bool(reasons)
    final_confidence = (
        round(min(1.0, max(first_pass.confidence, second_pass.confidence) + 0.05), 2)
        if not disagreements
        else round(min(first_pass.confidence, second_pass.confidence), 2)
    )

    return VerificationResult(
        app=first_pass.app,
        first_pass=first_pass,
        catalog_check=catalog_check,
        second_pass=second_pass,
        disagreements=disagreements,
        needs_human_review=needs_human_review,
        review_reason="; ".join(reasons) if reasons else "both signals agree",
        final_confidence=final_confidence,
    )
