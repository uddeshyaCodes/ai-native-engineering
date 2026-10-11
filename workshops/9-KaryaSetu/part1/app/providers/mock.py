"""
A fake provider.

Why it exists: you can demo the whole service with no API key and no spend,
and it proves the seam is real rather than decorative.
"""

from __future__ import annotations

import time

from . import Completion

_CANNED = (
    "Overall fit: strong. Matches: ships production Python services end to "
    "end; comfortable with typed API contracts. Gap: no explicit large-scale "
    "data pipeline experience."
)


class MockProvider:
    name = "mock"
    model = "mock-1"

    def complete(self, *, system: str, user: str) -> Completion:
        time.sleep(0.3)  # so latency behaves like the real thing
        return Completion(text=_CANNED, model=self.model, provider=self.name)
