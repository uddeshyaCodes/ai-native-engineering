"""
The schema the model must fill in -- and the rules a schema cannot express.

Week 2: your `description=` strings are PROMPT, serialised straight into the
JSON Schema handed to the model.

Week 3 adds the third layer of the contract. A JSON Schema can say "an integer
between 0 and 100". It cannot say "and the verdict must AGREE with that
integer". Those are INVARIANTS, and they live in validators, in code, where
they cannot be argued with:

    the system prompt   says the rule, in words, for the model
    the validators      enforce the rule, in code, for the machine
    the evals           measure how often the model obeys

One deliberate omission: `match_score` does NOT say "be strict, do not
inflate". Calibration is the system prompt's job in this part. Had we left it
in the field description, the schema would already be nudging the model and you
could not tell what the system prompt was contributing.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

from pydantic import BaseModel, Field, model_validator

# The prompt (prompts/fit_v2.md) states these bands in words. This dict is the
# same fact, enforced. A test checks the two still agree.
SCORE_BANDS: dict[str, tuple[int, int]] = {
    "strong_match": (70, 100),
    "possible_match": (35, 69),
    "weak_match": (0, 34),
}


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
            "requirements with direct evidence in the notes."
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

    @model_validator(mode="after")
    def _verdict_agrees_with_score(self) -> FitReport:
        low, high = SCORE_BANDS[self.verdict]
        if not low <= self.match_score <= high:
            raise ValueError(
                f"verdict {self.verdict!r} contradicts match_score "
                f"{self.match_score} (that verdict means {low}-{high})"
            )
        return self

    @model_validator(mode="after")
    def _table_supports_verdict(self) -> FitReport:
        missing = sum(s.strength == "missing" for s in self.skills)
        if self.verdict == "strong_match" and missing * 2 > len(self.skills):
            raise ValueError(
                f"strong_match, but {missing} of {len(self.skills)} requirements are missing"
            )
        return self


class FitReportResponse(BaseModel):
    """
    What OUR api returns -- deliberately a different class. FitReport is
    shaped for the model; this one carries provenance the model has no
    business inventing. New this week: `prompt_version`, so any answer can be
    traced back to the exact prompt that produced it.
    """

    report: FitReport
    provider: str
    model: str
    prompt_version: str
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
