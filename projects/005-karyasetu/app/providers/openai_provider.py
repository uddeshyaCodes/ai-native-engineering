"""
OpenAI adapter.

response.choices[0].message.content holds the answer. The system prompt is
just another message in the list, with role="system".
"""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import openai
from openai import OpenAI

from . import Completion, ProviderError


class OpenAIProvider:
    name = "openai"

    def __init__(self, settings) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.model = settings.openai_model
        self.s = settings
        self.client = OpenAI(api_key=settings.openai_api_key,base_url="https://api.groq.com/openai/v1")

    def complete(self, *, system: str, user: str) -> Completion:
        """Complete as of Part 1."""
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
        """Complete as of Part 2."""
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
        self, *, system: str, user: str, schema: dict[str, Any], name: str
    ) -> dict[str, Any]:
        """Ask for JSON conforming to `schema` via constrained decoding (`strict: True`)."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
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

        content = response.choices[0].message.content
        if not content:
            raise ProviderError("No content returned from OpenAI")
        return json.loads(content)
