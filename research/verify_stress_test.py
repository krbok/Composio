"""Runs Stage-2 verification against an existing Stage-1 run
(out/stress_test.json), so the two stages can be inspected independently.

Usage: python -m research.verify_stress_test
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv

from research.schema import Finding
from research.stress_test import STRESS_TEST_APPS
from research.verify import verify_finding

FIRST_PASS_PATH = Path(__file__).resolve().parent.parent / "out" / "stress_test.json"
OUT_PATH = Path(__file__).resolve().parent.parent / "out" / "verified_stress_test.json"

HINTS = {app: hint for app, _category, hint, _why in STRESS_TEST_APPS}


async def main() -> None:
    load_dotenv()
    first_pass_rows = json.loads(FIRST_PASS_PATH.read_text())

    results = []
    needs_review = 0
    for row in first_pass_rows:
        finding = Finding.model_validate(row)
        hint = HINTS[finding.app]
        print(f"\n=== Verifying {finding.app} ===")
        result = await verify_finding(finding, hint)
        results.append(result.model_dump(mode="json"))

        print(f"catalog check: {result.catalog_check.model_dump()}")
        if result.disagreements:
            for d in result.disagreements:
                print(f"  DISAGREE on {d.field}: first-pass={d.first_pass!r} vs browser-pass={d.second_pass!r}")
        else:
            print("  no disagreements")
        print(f"needs_human_review={result.needs_human_review} ({result.review_reason})")
        print(f"confidence: {finding.confidence} -> {result.final_confidence}")
        if result.needs_human_review:
            needs_review += 1

    OUT_PATH.write_text(json.dumps(results, indent=2))
    print(f"\n{len(results) - needs_review}/{len(results)} rows confirmed by both signals (auto-high-confidence).")
    print(f"{needs_review}/{len(results)} rows flagged for human review.")
    print(f"Wrote {OUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
