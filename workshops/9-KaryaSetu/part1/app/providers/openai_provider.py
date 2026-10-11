"""
OpenAI adapter.

response.choices[0].message.content holds the answer. The system prompt is
just another message in the list, with role="system".
"""

from __future__ import annotations

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
        # ------------------------------------------------------------------
        # TODO 1: call OpenAI's chat completions API.
        #
        # Call self.client.chat.completions.create() with a messages list
        # holding a system message and a user message, plus self.s.max_tokens
        # and self.s.temperature. The answer lives at
        # response.choices[0].message.content -- it can be None, so guard it
        # -- and belongs in a Completion. Catch openai.APIError and re-raise
        # it as a ProviderError, so no vendor exception ever leaves this
        # adapter.
        # ------------------------------------------------------------------
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user}
                ],
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature
            )
        except openai.APIError as e:
            raise ProviderError(f"OpenAI API error: {e}")
            
        content = response.choices[0].message.content

        if not content:
            raise ProviderError("No content returned from OpenAI")

        return Completion(
            text=content,
            model=self.model,
            provider=self.name
        )
