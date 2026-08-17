"""Stage-1 research across all 100 apps.

Resumable and incrementally saved: every completed row (success or failure)
is written to disk immediately, so a rate limit, crash, or Ctrl-C partway
through loses nothing -- re-running this script picks up wherever it left
off by skipping apps already present in out/all_100.json.

Usage: python -m research.run_all [--concurrency N]
"""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv

from research.agent import AgentDidNotSubmitError, research_app
from research.apps_100 import APPS_100

OUT_PATH = Path(__file__).resolve().parent.parent / "out" / "all_100.json"
FAILURES_PATH = Path(__file__).resolve().parent.parent / "out" / "all_100_failures.json"


def _load(path: Path) -> dict:
    if path.exists():
        return {row["app"]: row for row in json.loads(path.read_text())}
    return {}


async def _worker(
    app: str,
    category: str,
    hint: str,
    index: int,
    total: int,
    results: dict,
    failures: dict,
    lock: asyncio.Lock,
    semaphore: asyncio.Semaphore,
) -> None:
    async with semaphore:
        try:
            finding = await research_app(app, category, hint)
            row = finding.model_dump(mode="json")
            async with lock:
                results[app] = row
                failures.pop(app, None)
                _flush(results, failures)
            print(f"[{index}/{total}] OK    {app}  (confidence={row['confidence']})")
        except AgentDidNotSubmitError as exc:
            async with lock:
                failures[app] = str(exc)
                _flush(results, failures)
            print(f"[{index}/{total}] FAIL  {app}  ({exc})")
        except Exception as exc:  # noqa: BLE001 -- log and keep the batch going
            async with lock:
                failures[app] = f"{type(exc).__name__}: {exc}"
                _flush(results, failures)
            print(f"[{index}/{total}] ERROR {app}  ({type(exc).__name__}: {exc})")


def _flush(results: dict, failures: dict) -> None:
    OUT_PATH.parent.mkdir(exist_ok=True)
    OUT_PATH.write_text(json.dumps(list(results.values()), indent=2))
    FAILURES_PATH.write_text(json.dumps(failures, indent=2))


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=3)
    args = parser.parse_args()

    load_dotenv()
    results = _load(OUT_PATH)
    failures: dict = json.loads(FAILURES_PATH.read_text()) if FAILURES_PATH.exists() else {}

    todo = [(app, category, hint) for app, category, hint in APPS_100 if app not in results]
    print(f"{len(results)}/{len(APPS_100)} already done. {len(todo)} remaining.")

    lock = asyncio.Lock()
    semaphore = asyncio.Semaphore(args.concurrency)
    total = len(APPS_100)

    tasks = [
        _worker(app, category, hint, len(results) + i + 1, total, results, failures, lock, semaphore)
        for i, (app, category, hint) in enumerate(todo)
    ]
    await asyncio.gather(*tasks)

    print(f"\nDone. {len(results)}/{total} succeeded, {len(failures)}/{total} failed.")
    if failures:
        print("Failed apps:", list(failures.keys()))


if __name__ == "__main__":
    asyncio.run(main())
