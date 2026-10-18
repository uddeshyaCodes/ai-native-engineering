"""
Anthropic adapter.

Complete as of Week 2. Three differences from OpenAI, and they are why this
file exists:
  1. `system` is a TOP-LEVEL parameter, not a message.
  2. `max_tokens` is REQUIRED.
  3. The reply is a LIST of typed content blocks, so we filter by type rather
     than indexing [0]. Below, one of those blocks is a tool call.

A fourth, new this week: there is no `temperature` here. The current Anthropic
SDK does not accept sampling parameters at all, so Week 2's `temperature=` line
now raises TypeError. Vendors add and remove knobs; that is exactly why a knob
lives INSIDE an adapter and never in your routes. (`Settings.temperature`
therefore only affects OpenAI.)
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

import anthropic
from anthropic import Anthropic

from . import Completion, Message, ProviderError


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, settings) -> None:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        self.model = settings.anthropic_model
        self.s = settings
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    def complete(self, *, system: str, user: str) -> Completion:
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.s.max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            )
        except anthropic.APIError as exc:
            raise ProviderError(str(exc)) from exc

        text = "".join(b.text for b in message.content if b.type == "text")
        return Completion(text=text, model=self.model, provider=self.name)

    def stream(self, *, system: str, user: str) -> Iterator[str]:
        try:
            with self.client.messages.stream(
                model=self.model,
                max_tokens=self.s.max_tokens,
                system=system,
                messages=[{"role": "user", "content": user}],
            ) as stream:
                yield from stream.text_stream
        except anthropic.APIError as exc:
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
        """
        Anthropic's portable answer to "give me JSON" is TOOL USE -- and the
        trick is that we never intend to run the tool. We define one whose
        input schema is our target shape, force the model to call it with
        `tool_choice`, and read its ARGUMENTS instead of its prose.

        Without `tool_choice`, the model may still answer in prose and you
        are back to parsing English -- forcing it is what makes this reliable.
        """
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.s.max_tokens,
                system=system,  # top-level here, NOT a message
                messages=[*history, {"role": "user", "content": user}],
                tools=[
                    {
                        "name": name,
                        "description": "Return the completed report.",
                        "input_schema": schema,
                    }
                ],
                tool_choice={"type": "tool", "name": name},
            )
        except anthropic.APIError as exc:
            raise ProviderError(str(exc)) from exc

        if message.stop_reason == "max_tokens":
            raise ProviderError("The model hit max_tokens mid-JSON. Raise MAX_TOKENS.")
        for block in message.content:
            if block.type == "tool_use":
                return block.input

        raise ProviderError("The model did not call the tool.")
