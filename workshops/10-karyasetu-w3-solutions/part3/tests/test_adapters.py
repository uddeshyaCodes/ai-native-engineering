"""
Do the vendor adapters build the right requests? Tested with NO network and NO
key: a fake HTTP transport plays the vendor and records what it was sent.

This is how you test code that talks to an API you do not want to call from CI.
"""

import json
from types import SimpleNamespace

import httpx
import httpx2  # the Anthropic SDK is built on httpx2 and rejects a plain httpx.Client
import pytest
from anthropic import Anthropic
from openai import OpenAI

from app.providers import ProviderError
from app.providers.anthropic_provider import AnthropicProvider
from app.providers.openai_provider import OpenAIProvider

SCHEMA = {"type": "object", "properties": {"x": {"type": "string"}}, "required": ["x"]}
HISTORY = [
    {"role": "user", "content": "example question"},
    {"role": "assistant", "content": '{"x": "example answer"}'},
]
SETTINGS = SimpleNamespace(
    openai_api_key="test", openai_base_url=None, openai_model="m",
    anthropic_api_key="test", anthropic_model="m", max_tokens=100, temperature=0.4,
)


def fake(handler):
    return httpx.Client(transport=httpx.MockTransport(handler))


def fake2(handler):
    return httpx2.Client(transport=httpx2.MockTransport(handler))


def openai_provider(seen, *, content='{"x": "hi"}', finish="stop", refusal=None):
    def handler(request):
        seen.append(json.loads(request.content))
        message = {"role": "assistant", "content": content, "refusal": refusal}
        return httpx.Response(200, json={
            "id": "c1", "object": "chat.completion", "created": 0, "model": "m",
            "choices": [{"index": 0, "message": message, "finish_reason": finish}],
        })

    p = OpenAIProvider(SETTINGS)
    p.client = OpenAI(api_key="test", base_url="http://fake/v1", http_client=fake(handler), max_retries=0)
    return p


def anthropic_provider(seen, *, stop="tool_use", blocks=None):
    blocks = blocks if blocks is not None else [
        {"type": "tool_use", "id": "t1", "name": "fit_report", "input": {"x": "hi"}}
    ]

    def handler(request):
        seen.append(json.loads(request.content))
        return httpx2.Response(200, json={
            "id": "m1", "type": "message", "role": "assistant", "model": "m",
            "content": blocks, "stop_reason": stop, "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        })

    p = AnthropicProvider(SETTINGS)
    p.client = Anthropic(api_key="test", base_url="http://fake", http_client=fake2(handler), max_retries=0)
    return p


# ---- OpenAI ---------------------------------------------------------------------------


def test_openai_puts_system_first_then_examples_then_the_question():
    seen = []
    result = openai_provider(seen).structured(
        system="SYS", user="Q", schema=SCHEMA, name="fit_report", history=HISTORY
    )
    assert result == {"x": "hi"}
    roles = [m["role"] for m in seen[0]["messages"]]
    assert roles == ["system", "user", "assistant", "user"]
    assert seen[0]["messages"][0]["content"] == "SYS"
    assert seen[0]["messages"][-1]["content"] == "Q"


def test_openai_asks_for_strict_json_schema():
    seen = []
    openai_provider(seen).structured(system="S", user="Q", schema=SCHEMA, name="fit_report")
    fmt = seen[0]["response_format"]
    assert fmt["type"] == "json_schema"
    assert fmt["json_schema"] == {"name": "fit_report", "schema": SCHEMA, "strict": True}


def test_openai_notices_output_cut_off_by_max_tokens():
    with pytest.raises(ProviderError, match="max_tokens"):
        openai_provider([], content='{"x": "cut o', finish="length").structured(
            system="S", user="Q", schema=SCHEMA, name="n"
        )


def test_openai_surfaces_a_refusal_instead_of_a_json_error():
    with pytest.raises(ProviderError, match="refused"):
        openai_provider([], content=None, refusal="no").structured(
            system="S", user="Q", schema=SCHEMA, name="n"
        )


# ---- Anthropic ---------------------------------------------------------------------------


def test_anthropic_system_is_top_level_and_examples_precede_the_question():
    seen = []
    result = anthropic_provider(seen).structured(
        system="SYS", user="Q", schema=SCHEMA, name="fit_report", history=HISTORY
    )
    assert result == {"x": "hi"}
    assert seen[0]["system"] == "SYS"
    assert [m["role"] for m in seen[0]["messages"]] == ["user", "assistant", "user"]
    assert seen[0]["messages"][-1]["content"] == "Q"


def test_anthropic_forces_the_tool_so_we_read_arguments_not_prose():
    seen = []
    anthropic_provider(seen).structured(system="S", user="Q", schema=SCHEMA, name="fit_report")
    assert seen[0]["tool_choice"] == {"type": "tool", "name": "fit_report"}
    assert seen[0]["tools"][0]["input_schema"] == SCHEMA
    assert seen[0]["max_tokens"] == 100  # required by Anthropic


def test_anthropic_notices_output_cut_off_by_max_tokens():
    with pytest.raises(ProviderError, match="max_tokens"):
        anthropic_provider([], stop="max_tokens").structured(system="S", user="Q", schema=SCHEMA, name="n")


def test_anthropic_without_a_tool_call_is_an_error_not_a_guess():
    prose = [{"type": "text", "text": "Sure! Here you go"}]
    with pytest.raises(ProviderError, match="did not call the tool"):
        anthropic_provider([], blocks=prose).structured(system="S", user="Q", schema=SCHEMA, name="n")
