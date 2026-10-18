"""
A fake provider.

Why it exists: you can demo the whole service with no API key and no spend,
and it proves the seam is real rather than decorative.

It cannot show you what a PROMPT does -- a mock has no opinions. What it CAN do
is prove your plumbing: that the right text is assembled, and that a valid
shape comes back. Whether the words actually work is what evals are for.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import Any

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

_CANNED_REPORT = {
    "verdict": "possible_match",
    "match_score": 62,
    "headline": "Strong service-ownership signal, thin evidence on data pipelines.",
    "skills": [
        {
            "requirement": "2+ years production Python",
            "evidence": "Two years at a logistics startup.",
            "strength": "strong",
        },
        {
            "requirement": "Strong async fundamentals",
            "evidence": "handled retries, timeouts and their flaky rate limits",
            "strength": "partial",
        },
        {
            "requirement": "REST APIs consumed by other teams",
            "evidence": "Wrote the OpenAPI spec the mobile team consumed.",
            "strength": "strong",
        },
        {"requirement": "Data pipelines at scale", "evidence": None, "strength": "missing"},
    ],
    "gaps": ["large-scale data pipeline ownership", "explicit leadership scope"],
}


class MockProvider:
    name = "mock"
    model = "mock-1"
    latency = 0.3  # seconds; the tests set this to 0

    def complete(self, *, system: str, user: str) -> Completion:
        time.sleep(self.latency)  # so latency behaves like the real thing
        return Completion(text=_CANNED, model=self.model, provider=self.name)

    def stream(self, *, system: str, user: str) -> Iterator[str]:
        """Deliberately slow -- a demo that finishes in 40ms shows nothing."""
        words = _CANNED_LETTER.split(" ")
        for i in range(0, len(words), 3):
            time.sleep(0.08)
            yield " ".join(words[i : i + 3]) + (" " if i + 3 < len(words) else "")

    def structured(
        self, *, system: str, user: str, schema: dict[str, Any], name: str
    ) -> dict[str, Any]:
        """Returns a canned object that already satisfies FitReport."""
        time.sleep(self.latency)
        return dict(_CANNED_REPORT)
