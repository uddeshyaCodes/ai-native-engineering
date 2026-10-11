"""
Anthropic adapter.

Three differences from OpenAI, and they are why this file exists:
  1. `system` is a TOP-LEVEL parameter, not a message.
  2. `max_tokens` is REQUIRED.
  3. The reply is a LIST of typed content blocks, so we filter by type rather
     than indexing [0].
"""

from __future__ import annotations

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
        # ------------------------------------------------------------------
        # TODO 2: call Anthropic's Messages API.
        #
        # Call self.client.messages.create() with max_tokens (required),
        # temperature, system passed as its own top-level keyword rather than
        # a message, and a messages list holding a single user message. The
        # reply comes back as a list of content blocks, not one string --
        # join together the ones with type == "text". Catch
        # anthropic.APIError and re-raise it as a ProviderError.
        # ------------------------------------------------------------------
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.s.max_tokens,
                temperature=self.s.temperature,
                system=system,
                messages=[{"role": "user", "content": user}]
            )
        except anthropic.APIError as e:
            raise ProviderError(f"Anthropic API error: {e}")
        
        content = "\n".join([block.text for block in response.content if block.type == "text"])
        if not content:
            raise ProviderError("No content returned from Anthropic")
        
        return Completion(
            text=content,
            model=self.model,
            provider=self.name
        )
