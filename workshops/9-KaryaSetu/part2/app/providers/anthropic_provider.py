"""
Anthropic adapter.

Three differences from OpenAI, and they are why this file exists:
  1. `system` is a TOP-LEVEL parameter, not a message.
  2. `max_tokens` is REQUIRED.
  3. The reply is a LIST of typed content blocks, so we filter by type rather
     than indexing [0].
"""

from __future__ import annotations

from collections.abc import Iterator

import anthropic
from anthropic import Anthropic

from . import Completion, ProviderError


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, settings) -> None:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        self.model = settings.anthropic_model
        self.s = settings
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    def complete(self, *, system: str, user: str) -> Completion:
        """Complete as of Part 1."""
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
        except anthropic.APIError as exc:
            raise ProviderError(str(exc)) from exc

        text = "".join(b.text for b in message.content if b.type == "text")
        return Completion(text=text, model=self.model, provider=self.name)

    def stream(self, *, system: str, user: str) -> Iterator[str]:
        """
        Given, for comparison with the OpenAI version you just wrote in
        TODO 2. Different ergonomics: no stream=True flag, a dedicated
        `messages.stream()` that is a CONTEXT MANAGER, and a ready-made
        `.text_stream` that already filters out the typed event feed
        (message_start, content_block_delta, ...) down to plain text.

        Why a context manager? If the client hangs up mid-generation, the
        underlying HTTP response still needs to be closed. `with` guarantees
        that instead of leaking a connection.
        """
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
                system=system,
                messages=[{"role": "user", "content": user}],
            ) as stream:
                yield from stream.text_stream
        except anthropic.APIError as exc:
            raise ProviderError(str(exc)) from exc
