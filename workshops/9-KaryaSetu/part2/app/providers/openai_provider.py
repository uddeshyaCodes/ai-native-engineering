"""
OpenAI adapter.

response.choices[0].message.content holds the answer. The system prompt is
just another message in the list, with role="system".
"""

from __future__ import annotations

from collections.abc import Iterator

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
        # ------------------------------------------------------------------
        # TODO 2: stream from OpenAI.
        #
        # Call self.client.chat.completions.create() the same way as
        # complete(), but add stream=True. The request change is one word,
        # but it changes the RETURN TYPE: you no longer get a response
        # object back, you get an iterator of chunks. Loop over it, skip any
        # chunk whose choices list is empty (a trailing usage-only chunk),
        # and yield chunk.choices[0].delta.content only when it is truthy --
        # it is None on the first chunk (which only announces the role) and
        # on the last one. Catch openai.APIError and re-raise it as a
        # ProviderError.
        # ------------------------------------------------------------------
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
                stream=True
            )
        except openai.APIError as exc:
            raise ProviderError(str(exc)) from exc

        try:
            for chunk in response:
                if not chunk.choices:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except openai.APIError as exc:
            raise ProviderError(str(exc)) from exc
