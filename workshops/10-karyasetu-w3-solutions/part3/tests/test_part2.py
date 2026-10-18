"""
Part 2 -- examples and reasoning.

TODO 1 (build_history) is checked by the `history_*` tests.
TODO 2 (with_reasoning) is checked by the `reasoning_*` tests.
Part 1's tests still run too: a new feature must not break an old contract.
"""

import json

import pytest

from app.evals.__main__ import evaluate, load_cases
from app.fit import FitReport, strictify, with_reasoning
from app.main import provider
from app.prompting import MAX_SHOTS, build_history, load_examples, render_user_message


@pytest.fixture
def examples():
    return load_examples()


# ---- TODO 1: build_history ----------------------------------------------------


def test_history_pairs_each_example_as_user_then_assistant(examples):
    history = build_history(examples[:3], include_reasoning=False)
    assert [m["role"] for m in history] == ["user", "assistant"] * 3


def test_history_zero_examples_is_zero_turns():
    assert build_history([], include_reasoning=False) == []


def test_history_user_turn_goes_through_the_live_renderer(examples):
    """Examples formatted differently from real input teach the model two formats."""
    ex = examples[0]
    history = build_history([ex], include_reasoning=False)
    assert history[0]["content"] == render_user_message(ex["job_description"], ex["experience_notes"])


def test_history_assistant_turn_is_the_ideal_answer_as_json(examples):
    ex = examples[1]
    answer = json.loads(build_history([ex], include_reasoning=True)[1]["content"])
    assert answer == ex["report"]


def test_history_drops_reasoning_when_the_schema_has_none(examples):
    answer = json.loads(build_history(examples[:1], include_reasoning=False)[1]["content"])
    assert "reasoning" not in answer, "the example shows a field the schema does not have"
    FitReport.model_validate(answer)  # and it is a valid public report


def test_history_keeps_reasoning_first_when_asked(examples):
    answer = json.loads(build_history(examples[:1], include_reasoning=True)[1]["content"])
    assert list(answer)[0] == "reasoning", "even the examples must think before they answer"


def test_history_does_not_mutate_the_examples(examples):
    before = json.dumps(examples)
    build_history(examples, include_reasoning=False)
    assert json.dumps(examples) == before, "you popped 'reasoning' off the shared example"


# ---- TODO 2: with_reasoning -----------------------------------------------------


def test_reasoning_field_comes_first():
    props = list(with_reasoning(FitReport).model_json_schema()["properties"])
    assert props[0] == "reasoning", f"order is {props}: put reasoning= before **fields"
    assert props.index("reasoning") < props.index("verdict") < props.index("match_score")


def test_reasoning_field_is_still_first_after_strictify():
    """This is the order the provider actually receives."""
    schema = strictify(with_reasoning(FitReport).model_json_schema())
    assert schema["required"][0] == "reasoning"


def test_reasoning_description_actually_tells_the_model_how_to_think():
    desc = with_reasoning(FitReport).model_json_schema()["properties"]["reasoning"]["description"]
    assert len(desc) >= 40, "a description is PROMPT -- say how to reason"


def test_derived_model_keeps_every_original_field_and_its_constraints():
    derived = with_reasoning(FitReport).model_json_schema()["properties"]
    original = FitReport.model_json_schema()["properties"]
    assert set(derived) - {"reasoning"} == set(original)
    assert derived["match_score"]["maximum"] == 100
    assert derived["skills"]["maxItems"] == 6


def test_deriving_a_model_does_not_touch_the_original():
    with_reasoning(FitReport)
    assert "reasoning" not in FitReport.model_fields


def test_derived_model_has_a_sensible_name():
    assert with_reasoning(FitReport).__name__ == "FitReportWithReasoning"


def test_every_example_is_a_valid_answer_to_the_schema_it_demonstrates(examples):
    derived = with_reasoning(FitReport)
    for ex in examples:
        derived.model_validate(ex["report"])
        FitReport.model_validate({k: v for k, v in ex["report"].items() if k != "reasoning"})


# ---- Given: the data ---------------------------------------------------------------


def test_there_are_as_many_examples_as_MAX_SHOTS(examples):
    assert len(examples) == MAX_SHOTS


def test_examples_never_appear_in_the_eval_set(examples):
    """Grading a prompt on its own examples is marking your own homework."""
    graded = {c["job_description"] for c in load_cases()}
    assert not graded & {e["job_description"] for e in examples}


# ---- Given: the endpoint ---------------------------------------------------------------


def test_the_public_report_never_carries_the_scratchpad(client, sample):
    body = client.post("/v1/fit-report?reasoning=true", json=sample).json()
    assert "reasoning" not in body["report"]
    assert body["scratchpad"] is None, "scratchpad is dev-mode only"


def test_dev_mode_returns_the_scratchpad(client, sample, debug_on):
    body = client.post("/v1/fit-report?reasoning=true", json=sample).json()
    assert body["reasoning"] is True and body["scratchpad"]


def test_the_response_says_how_it_was_produced(client, sample):
    body = client.post("/v1/fit-report?shots=2&reasoning=true", json=sample).json()
    assert (body["prompt_version"], body["shots"], body["reasoning"]) == ("v2", 2, True)


def test_shots_are_bounded(client, sample):
    assert client.post(f"/v1/fit-report?shots={MAX_SHOTS + 1}", json=sample).status_code == 422


def test_preview_shows_examples_as_earlier_turns_and_reasoning_first(client, sample, debug_on):
    body = client.post("/v1/fit-report/preview?shots=2&reasoning=true", json=sample).json()
    assert len(body["history"]) == 4
    assert body["schema_fields"][0] == "reasoning"


def test_examples_cost_tokens_on_every_call(client, sample, debug_on):
    def tokens(shots):
        r = client.post(f"/v1/fit-report/preview?shots={shots}", json=sample)
        return r.json()["approx_input_tokens"]

    assert tokens(0) < tokens(2) < tokens(4)


def test_the_eval_harness_runs_end_to_end_offline():
    cases = load_cases()
    results = evaluate(cases, version="v2", shots=MAX_SHOTS, reasoning=True, workers=2)
    assert len(results) == len(cases) == 10
    assert all(r.got is not None for r in results), [r.problem for r in results]
    assert provider.name == "mock"
