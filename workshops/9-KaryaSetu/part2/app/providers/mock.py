"""
A fake provider.

Why it exists: you can demo the whole service with no API key and no spend,
and it proves the seam is real rather than decorative.
"""

from __future__ import annotations

import time
from collections.abc import Iterator

from . import Completion

_CANNED = (
    "Overall fit: strong. Matches: ships production Python services end to "
    "end; comfortable with typed API contracts. Gap: no explicit large-scale "
    "data pipeline experience."
)

_CANNED_LETTER = (
    "Dear Hiring Team,\n\n"
    "I spent the last two years owning the service that sat between our "
    "product and a carrier rate API that went down more often than anyone "
    "liked. That taught me the parts of this role you are actually hiring "
    "for: retries that do not stampede, timeouts chosen on purpose, and an "
    "API contract other teams can build against without asking me questions "
    "in Slack.\n\n"
    "I wrote the OpenAPI spec our mobile team consumed, and the latency "
    "dashboards we used to argue about it. I would like to do that here, "
    "against model providers instead of carriers.\n\n"
    "Thanks for your time.\n"
)


class MockProvider:
    name = "mock"
    model = "mock-1"

    def complete(self, *, system: str, user: str) -> Completion:
        time.sleep(0.3)  # so latency behaves like the real thing
        return Completion(text=_CANNED, model=self.model, provider=self.name)

    def stream(self, *, system: str, user: str) -> Iterator[str]:
        """Deliberately slow -- a demo that finishes in 40ms shows nothing."""
        words = _CANNED_LETTER.split(" ")
        for i in range(0, len(words), 3):
            time.sleep(0.08)
            yield " ".join(words[i : i + 3]) + (" " if i + 3 < len(words) else "")
