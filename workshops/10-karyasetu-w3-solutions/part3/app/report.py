"""
Assemble a prompt, run it, validate the result.

Both the API route AND the eval harness call these two functions. That is
deliberate: an eval that exercises a different code path from production
measures a different product.

Two knobs, each visible in the Prompt BEFORE anything is sent:

    shots      how many worked examples ride along as earlier turns
    reasoning  whether the model must think (in a field that comes FIRST)
               before it commits to a verdict
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel

from .fit import FitReport, strictify, with_reasoning
from .prompting import (
    build_history,
    load_examples,
    load_prompt,
    render_user_message,
)
from .providers import LLMProvider, Message


@dataclass(frozen=True)
class Prompt:
    """Everything that will be sent to the model. Inspectable BEFORE the call."""

    version: str
    system: str
    history: list[Message] = field(default_factory=list)
    user: str = ""
    shots: int = 0
    reasoning: bool = False
    schema_model: type[BaseModel] = FitReport


@dataclass(frozen=True)
class Run:
    report: FitReport
    scratchpad: str | None  # the model's reasoning, if it was asked for any


def assemble_prompt(
    job_description: str,
    experience_notes: str,
    *,
    version: str,
    shots: int = 0,
    reasoning: bool = False,
) -> Prompt:
    return Prompt(
        version=version,
        system=load_prompt("fit", version),
        # Zero-shot never touches build_history: the baseline product works
        # before the first example is wired in.
        history=(
            build_history(load_examples()[:shots], include_reasoning=reasoning)
            if shots
            else []
        ),
        user=render_user_message(job_description, experience_notes),
        shots=shots,
        reasoning=reasoning,
        schema_model=with_reasoning(FitReport) if reasoning else FitReport,
    )


def generate_report(provider: LLMProvider, prompt: Prompt) -> Run:
    schema = strictify(prompt.schema_model.model_json_schema())
    raw = provider.structured(
        system=prompt.system,
        history=prompt.history,
        user=prompt.user,
        schema=schema,
        name="fit_report",
    )
    parsed = prompt.schema_model.model_validate(raw)
    scratchpad = getattr(parsed, "reasoning", None)

    # The scratchpad is for the model, not for the client: the PUBLIC contract
    # is still FitReport. Re-validating through it also applies the invariants
    # (verdict vs score, table vs verdict), which live on FitReport, not on the
    # derived model. Constrained decoding guarantees SHAPE; only this line
    # knows that 137 is not a match_score. Validate anyway.
    report = FitReport.model_validate(parsed.model_dump(exclude={"reasoning"}))
    return Run(report=report, scratchpad=scratchpad)
