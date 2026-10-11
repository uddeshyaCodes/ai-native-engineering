"""
The schema the model must fill in.

Everything you know about Pydantic applies unchanged. What is new: your
`description=` strings stop being documentation and start being PROMPT --
they are serialised straight into the JSON Schema handed to the model.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    """One requirement from the posting, judged against the notes."""

    requirement: str = Field(
        max_length=120, description="A requirement from the posting, under fifteen words."
    )
    evidence: str | None = Field(
        default=None,
        max_length=200,
        description=(
            "The line in the candidate's notes that satisfies this "
            "requirement. Null if there is none. Never invent evidence."
        ),
    )
    strength: Literal["strong", "partial", "missing"]


class FitReport(BaseModel):
    """The object the frontend renders. No prose parsing, ever."""

    verdict: Literal["strong_match", "possible_match", "weak_match"]
    match_score: int = Field(
        ge=0,
        le=100,
        description=(
            "0-100. Roughly the percentage of the posting's hard "
            "requirements with direct evidence in the notes. Be strict; do "
            "not inflate."
        ),
    )
    headline: str = Field(
        max_length=140, description="One sentence a hiring manager could read in three seconds."
    )
    skills: list[SkillMatch] = Field(
        min_length=3, max_length=6, description="Three to six requirements, most important first."
    )
    gaps: list[str] = Field(
        max_length=4,
        description="Requirements with no supporting evidence. Empty list if there are none.",
    )


class FitReportResponse(BaseModel):
    """
    What OUR api returns -- deliberately a different class. FitReport is
    shaped for the model; this one carries provenance the model has no
    business inventing.
    """

    report: FitReport
    provider: str
    model: str
    latency_ms: int


def strictify(schema: dict[str, Any]) -> dict[str, Any]:
    """
    Bridge Pydantic's JSON Schema to what OpenAI's strict mode accepts.

    Strict mode demands every property in `required` and
    `additionalProperties: false` on every object. Pydantic emits neither --
    correctly, since a field with a default genuinely is not required.
    Optionality does not disappear, it MOVES: into the type, as
    `anyOf: [{"type": "string"}, {"type": "null"}]`. The key is always
    present; the value may be null. Pydantic already writes `str | None`
    that way.
    """
    schema = deepcopy(schema)
    _walk(schema)
    for definition in schema.get("$defs", {}).values():
        _walk(definition)  # nested models live here -- easy to miss
    return schema


def _walk(node: Any) -> None:
    if isinstance(node, dict):
        if node.get("type") == "object" and "properties" in node:
            node["additionalProperties"] = False
            node["required"] = list(node["properties"].keys())
        for value in node.values():
            _walk(value)
    elif isinstance(node, list):
        for item in node:
            _walk(item)


if __name__ == "__main__":  # python -m app.fit
    import json

    raw = FitReport.model_json_schema()
    print("=== as Pydantic emits it ===")
    print(json.dumps(raw, indent=2))
    print("\n=== as the provider needs it ===")
    print(json.dumps(strictify(raw), indent=2))
