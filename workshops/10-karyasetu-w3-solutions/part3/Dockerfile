# syntax=docker/dockerfile:1
#
# One Dockerfile, two targets:
#
#   dev   docker build --target dev  .   code arrives by bind mount, reload on
#   prod  docker build --target prod .   code baked in, non-root, no reload
#
# Compose builds `dev`. Everything both need lives in `base`.

FROM python:3.12-slim AS base

# PYTHONUNBUFFERED       print() reaches `docker logs` immediately. Without it
#                        Python buffers stdout when it is not a terminal -- the
#                        same buffering trap as Week 2's streaming.
# PYTHONDONTWRITEBYTECODE  no __pycache__ litter on your bind-mounted folder.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# ---------------------------------------------------------------------------
# TODO 1a: install the dependencies in their OWN layer.
#
# Docker caches each instruction as a layer and rebuilds from the first line
# that changed. Your code changes every few minutes; your dependencies change
# once a week. So copy ONLY requirements.txt first, install it, and copy the
# code later. (Get this order wrong and every one-line edit reinstalls
# fastapi, openai and anthropic.)
#
# Two lines: COPY requirements.txt, then RUN pip install -r requirements.txt.
# ---------------------------------------------------------------------------
COPY requirements.txt .
RUN pip install -r requirements.txt
# -- end of solution

# No curl in a slim image, but Python is right here. Compose uses this status.
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"]


# ---- dev: code is bind-mounted by compose.yaml, so nothing to COPY ----------
FROM base AS dev

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# ---------------------------------------------------------------------------
# TODO 1b: the dev-mode command.
#
# Write CMD in EXEC form (a JSON list) so uvicorn is PID 1 and receives
# `docker stop`'s SIGTERM. Run "app.main:app" on port 8000, and:
#
#   --host 0.0.0.0     "127.0.0.1" inside a container means the container
#                      ITSELF. Bind to it and `-p 8000:8000` can never reach
#                      you. Listen on all interfaces.
#   --reload --reload-dir app     restart when a .py file changes
#
# (Prompt files need no reload: load_prompt() reads them on every request.)
# ---------------------------------------------------------------------------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "app"]
# -- end of solution


# ---- prod: everything baked in, nothing writable, nobody is root ------------
FROM base AS prod

COPY app ./app
RUN useradd --uid 10001 --create-home --shell /usr/sbin/nologin appuser
USER 10001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
