"""
Server-Sent Events, from first principles.

Every event is a few `field: value` lines followed by a BLANK line -- that
blank line is the entire protocol. It is what tells the browser "this event
is complete, dispatch it now".

    event: token
    data: {"text": "Dear hiring"}
    <blank line>
"""

from __future__ import annotations

import json
from typing import Any


def sse_event(data: Any, *, event: str) -> str:
    """The classic bug is forgetting the trailing blank line: bytes arrive,
    nothing errors, and the browser fires zero events."""
    return f"event: {event}\ndata: {json.dumps(data)}\n\n"


# Not decoration:
#   cache-control      an intermediate cache must never store a live stream
#   x-accel-buffering  nginx buffers proxied responses by default -- without
#                      this your stream works on localhost and silently
#                      stops streaming in production
SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "X-Accel-Buffering": "no",
}
