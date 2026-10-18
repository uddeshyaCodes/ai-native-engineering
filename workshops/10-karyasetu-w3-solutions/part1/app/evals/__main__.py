"""
Evals: the test suite for a prompt.

    python -m app.evals                 # current default prompt
    python -m app.evals --prompt v1     # compare against an older version
    LLM_PROVIDER=openai python -m app.evals --prompt v2

A prompt change is a code change, and code changes get tests. This runs every
case in cases.jsonl through the SAME assemble_prompt() / generate_report() the
API uses, and scores the verdicts against labels a human wrote.

Read the numbers honestly:
  * Ten cases is a smoke test, not a benchmark. One flipped case is 10 points.
  * A model is not deterministic. Run it twice. If the score moves, that is
    the finding.
  * Against the MOCK provider this only proves the plumbing works. A mock has
    no opinions about prompts.
"""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from ..main import provider
from ..prompting import DEFAULT_PROMPT_VERSION
from ..providers import ProviderError
from ..report import assemble_prompt, generate_report

CASES = Path(__file__).parent / "cases.jsonl"
ORDER = {"weak_match": 0, "possible_match": 1, "strong_match": 2}


@dataclass
class Result:
    case: dict
    got: str | None  # None => the contract was broken or the call failed
    score: int | None
    problem: str | None = None

    @property
    def ok(self) -> bool:
        return self.got == self.case["expected"]

    @property
    def catastrophic(self) -> bool:
        """Two full steps away: strong for a weak candidate, or the reverse."""
        return self.got is not None and abs(ORDER[self.got] - ORDER[self.case["expected"]]) == 2


def load_cases() -> list[dict]:
    return [json.loads(line) for line in CASES.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_case(case: dict, *, version: str) -> Result:
    prompt = assemble_prompt(
        case["job_description"], case["experience_notes"], version=version
    )
    try:
        run = generate_report(provider, prompt)
    except ValidationError as exc:
        return Result(case, None, None, "broke the contract: " + "; ".join(e["msg"] for e in exc.errors()))
    except ProviderError as exc:
        return Result(case, None, None, f"provider error: {exc.message}")
    return Result(case, run.report.verdict, run.report.match_score)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--prompt", default=DEFAULT_PROMPT_VERSION, help="prompt version, e.g. v1")
    parser.add_argument("--workers", type=int, default=4, help="parallel calls")
    args = parser.parse_args()

    cases = load_cases()
    print(f"provider={provider.name} model={provider.model} prompt={args.prompt} cases={len(cases)}")
    if provider.name == "mock":
        print("!! MOCK provider: this checks the plumbing, NOT the prompt. Set LLM_PROVIDER.\n")

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        results = list(pool.map(lambda c: run_case(c, version=args.prompt), cases))

    print(f"{'case':<24}{'expected':<16}{'got':<16}{'score':>5}  result")
    for r in results:
        mark = "ok" if r.ok else ("CATASTROPHIC" if r.catastrophic else "miss")
        if r.got is None:
            mark = f"INVALID ({r.problem})"
        print(f"{r.case['id']:<24}{r.case['expected']:<16}{r.got or '-':<16}{r.score if r.score is not None else '-':>5}  {mark}")

    correct = sum(r.ok for r in results)
    print(
        f"\naccuracy {correct}/{len(results)}   "
        f"catastrophic {sum(r.catastrophic for r in results)}   "
        f"invalid {sum(r.got is None for r in results)}"
    )


if __name__ == "__main__":
    main()
