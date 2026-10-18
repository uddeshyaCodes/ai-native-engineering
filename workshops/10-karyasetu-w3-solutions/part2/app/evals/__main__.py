"""
Evals: the test suite for a prompt.

    python -m app.evals                          # v2, zero-shot, no reasoning
    python -m app.evals --prompt v1              # compare against an older version
    python -m app.evals --shots 4 --reasoning    # one configuration
    python -m app.evals --grid                   # the 2x2: shots x reasoning
    LLM_PROVIDER=openai python -m app.evals --grid

A prompt change is a code change, and code changes get tests. This runs every
case in cases.jsonl through the SAME assemble_prompt() / generate_report() the
API uses, and scores the verdicts against labels a human wrote.

Read the numbers honestly:
  * Ten cases is a smoke test, not a benchmark. One flipped case is 10 points.
  * A model is not deterministic. Run it twice. If the score moves, that is
    the finding.
  * The worked examples in prompts/fit_examples.json are NEVER in cases.jsonl.
    Grading a prompt on its own examples is marking your own homework.
  * Against the MOCK provider this only proves the plumbing works. A mock has
    no opinions about prompts.
"""

from __future__ import annotations

import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from ..main import provider
from ..prompting import DEFAULT_PROMPT_VERSION, MAX_SHOTS
from ..providers import ProviderError
from ..report import assemble_prompt, generate_report

CASES = Path(__file__).parent / "cases.jsonl"
ORDER = {"weak_match": 0, "possible_match": 1, "strong_match": 2}


@dataclass
class Result:
    case: dict
    got: str | None  # None => the contract was broken or the call failed
    score: int | None
    ms: int
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


def run_case(case: dict, *, version: str, shots: int, reasoning: bool) -> Result:
    prompt = assemble_prompt(
        case["job_description"],
        case["experience_notes"],
        version=version,
        shots=shots,
        reasoning=reasoning,
    )
    started = time.perf_counter()
    try:
        run = generate_report(provider, prompt)
    except ValidationError as exc:
        problem = "broke the contract: " + "; ".join(e["msg"] for e in exc.errors())
        return Result(case, None, None, _ms(started), problem)
    except ProviderError as exc:
        return Result(case, None, None, _ms(started), f"provider error: {exc.message}")
    return Result(case, run.report.verdict, run.report.match_score, _ms(started))


def _ms(started: float) -> int:
    return int((time.perf_counter() - started) * 1000)


def evaluate(cases, *, version, shots, reasoning, workers) -> list[Result]:
    with ThreadPoolExecutor(max_workers=workers) as pool:
        return list(
            pool.map(
                lambda c: run_case(c, version=version, shots=shots, reasoning=reasoning), cases
            )
        )


def summarise(results: list[Result]) -> str:
    n = len(results)
    avg = sum(r.ms for r in results) / n / 1000
    return (
        f"{sum(r.ok for r in results)}/{n} right, "
        f"{sum(r.catastrophic for r in results)} catastrophic, "
        f"{sum(r.got is None for r in results)} invalid, "
        f"~{avg:.1f}s/call"
    )


def print_table(results: list[Result]) -> None:
    print(f"{'case':<24}{'expected':<16}{'got':<16}{'score':>5}  result")
    for r in results:
        mark = "ok" if r.ok else ("CATASTROPHIC" if r.catastrophic else "miss")
        if r.got is None:
            mark = f"INVALID ({r.problem})"
        score = r.score if r.score is not None else "-"
        print(f"{r.case['id']:<24}{r.case['expected']:<16}{r.got or '-':<16}{score:>5}  {mark}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the KaryaSetu prompt evals.")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT_VERSION, help="prompt version, e.g. v1")
    parser.add_argument("--shots", type=int, default=0, choices=range(MAX_SHOTS + 1))
    parser.add_argument("--reasoning", action="store_true", help="reasoning-first schema")
    parser.add_argument("--grid", action="store_true", help="run shots{0,max} x reasoning{off,on}")
    parser.add_argument("--workers", type=int, default=4, help="parallel calls")
    args = parser.parse_args()

    cases = load_cases()
    print(f"provider={provider.name} model={provider.model} prompt={args.prompt} cases={len(cases)}")
    if provider.name == "mock":
        print("!! MOCK provider: this checks the plumbing, NOT the prompt. Set LLM_PROVIDER.\n")

    if not args.grid:
        results = evaluate(
            cases, version=args.prompt, shots=args.shots, reasoning=args.reasoning, workers=args.workers
        )
        print_table(results)
        print(f"\nshots={args.shots} reasoning={'on' if args.reasoning else 'off'}: {summarise(results)}")
        return

    print(f"{'':<12}{'reasoning OFF':<44}reasoning ON")
    for shots in (0, MAX_SHOTS):
        cells = []
        for reasoning in (False, True):
            results = evaluate(
                cases, version=args.prompt, shots=shots, reasoning=reasoning, workers=args.workers
            )
            cells.append(summarise(results))
        print(f"{shots}-shot{'':<6}{cells[0]:<44}{cells[1]}")


if __name__ == "__main__":
    main()
