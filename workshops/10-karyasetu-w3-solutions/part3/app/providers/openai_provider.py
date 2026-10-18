"""
OpenAI adapter.

Complete as of Week 2 -- nothing here is a TODO this week. Two small additions
worth reading, because they are what "works in a demo" vs "works in production"
looks like:

  * `base_url` -- any OpenAI-compatible endpoint (OpenRouter, Groq, a local
    server) works through this same adapter. Strict JSON-schema support varies
    by model, so check before you rely on it.
  * `structured()` now notices when the model was cut off by `max_tokens`.
    Truncated JSON is not "a bit wrong", it is unparseable -- and a longer
    prompt (more examples, a reasoning field) makes that more likely.
"""

from __future__ import annotations

import json
from collections.abc import Iterator, Sequence
from typing import Any

import openai
from openai import OpenAI

from . import Completion, Message, ProviderError


class OpenAIProvider:
    name = "openai"

    def __init__(self, settings) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.model = settings.openai_model
        self.s = settings
        self.client = OpenAI(
            api_key=settings.openai_api_key, base_url=settings.openai_base_url
        )

    def complete(self, *, system: str, user: str) -> Completion:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
            )
        except openai.APIError as exc:
            raise ProviderError(str(exc)) from exc

        return Completion(
            text=response.choices[0].message.content or "",
            model=self.model,
            provider=self.name,
        )

    def stream(self, *, system: str, user: str) -> Iterator[str]:
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
                stream=True,
            )
            for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta
        except openai.APIError as exc:
            raise ProviderError(str(exc)) from exc

    def structured(
        self,
        *,
        system: str,
        user: str,
        schema: dict[str, Any],
        name: str,
        history: Sequence[Message] = (),
    ) -> dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                # system is a message here; the examples sit between it and
                # the real question, as turns the model "already had".
                messages=[
                    {"role": "system", "content": system},
                    *history,
                    {"role": "user", "content": user},
                ],
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
                response_format={
                    "type": "json_schema",
                    "json_schema": {"name": name, "schema": schema, "strict": True},
                },
            )
        except openai.APIError as exc:
            raise ProviderError(str(exc)) from exc

        choice = response.choices[0]
        if choice.finish_reason == "length":
            raise ProviderError("The model hit max_tokens mid-JSON. Raise MAX_TOKENS.")
        refusal = getattr(choice.message, "refusal", None)
        if refusal:
            raise ProviderError(f"The model refused: {refusal}")
        try:
            return json.loads(choice.message.content)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ProviderError("The model did not return valid JSON.") from exc
