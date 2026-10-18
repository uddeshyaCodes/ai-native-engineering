"""
The seam: one interface, many vendors.

Every vendor SDK has its own request shape, response shape and exception
hierarchy. If those leak into your routes, your app is married to one vendor.
So we define ONE narrow interface and write a thin adapter per vendor behind
it. Only the two provider files below import a vendor SDK -- nothing else
does.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Any, Literal, Protocol, TypedDict


@dataclass
class Completion:
    """A finished generation, normalised across vendors."""

    text: str
    model: str
    provider: str


class Message(TypedDict):
    """One earlier turn of the conversation. The API is stateless: 'earlier'
    exists only because we send it again every time."""

    role: Literal["user", "assistant"]
    content: str


class ProviderError(Exception):
    """
    Our own vendor-neutral error.

    Adapters catch SDK-specific exceptions and re-raise this, so the rest of
    the app knows only this one type -- not openai's exceptions and
    anthropic's exceptions and mock's exceptions.
    """

    def __init__(self, message: str, *, status: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status = status


class LLMProvider(Protocol):
    """The only LLM surface our application code depends on."""

    name: str
    model: str

    def complete(self, *, system: str, user: str) -> Completion:
        """Send one prompt, wait for the whole answer, return it."""
        ...

    def stream(self, *, system: str, user: str) -> Iterator[str]:
        """Send one prompt, yield text fragments as they are produced."""
        ...

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
        Send one prompt, get back a dict conforming to `schema`.

        `history` holds earlier turns, oldest first, that come BEFORE `user`.
        Few-shot examples travel there, as (user, assistant) pairs. The system
        prompt stays separate on purpose: OpenAI wants it as a message,
        Anthropic as a top-level parameter -- that is the adapters' problem.

        Returns a plain dict, NOT a Pydantic model -- deliberately. The
        adapter's job ends at "JSON of roughly the right shape". Turning
        that into a trusted FitReport is model_validate's job, above the
        seam.
        """
        ...


def build_provider(settings) -> LLMProvider:
    """One switch, one place. Vendor SDKs are imported lazily, so choosing
    'mock' never even imports openai or anthropic."""
    if settings.llm_provider == "mock":
        from .mock import MockProvider

        return MockProvider()
    if settings.llm_provider == "openai":
        from .openai_provider import OpenAIProvider

        return OpenAIProvider(settings)
    if settings.llm_provider == "anthropic":
        from .anthropic_provider import AnthropicProvider

        return AnthropicProvider(settings)
    raise RuntimeError(f"Unknown provider: {settings.llm_provider}")
