"""
Assemble a prompt, run it, validate the result.

Both the API route AND the eval harness call these two functions. That is
deliberate: an eval that exercises a different code path from production
measures a different product.
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

from .fit import FitReport, strictify
from .prompting import load_prompt, render_user_message
from .providers import LLMProvider


@dataclass(frozen=True)
class Prompt:
    """Everything that will be sent to the model. Inspectable BEFORE the call."""

    version: str
    system: str
    user: str
    schema_model: type[BaseModel]


@dataclass(frozen=True)
class Run:
    report: FitReport


def assemble_prompt(
    job_description: str, experience_notes: str, *, version: str
) -> Prompt:
    return Prompt(
        version=version,
        system=load_prompt("fit", version),
        user=render_user_message(job_description, experience_notes),
        schema_model=FitReport,
    )


def generate_report(provider: LLMProvider, prompt: Prompt) -> Run:
    schema = strictify(prompt.schema_model.model_json_schema())
    raw = provider.structured(
        system=prompt.system, user=prompt.user, schema=schema, name="fit_report"
    )
    # Constrained decoding guarantees the SHAPE. Only this line knows that
    # 137 is not a match_score, or that a strong_match cannot have most of its
    # requirements missing. Validate anyway.
    return Run(report=FitReport.model_validate(raw))
