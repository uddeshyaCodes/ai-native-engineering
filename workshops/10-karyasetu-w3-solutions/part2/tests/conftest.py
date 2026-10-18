"""Tests never touch a real vendor: force the mock BEFORE the app is imported."""

import os

os.environ["LLM_PROVIDER"] = "mock"  # environment variables beat .env
os.environ.pop("APP_DEBUG", None)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.main import app, get_settings  # noqa: E402
from app.providers.mock import MockProvider  # noqa: E402

SAMPLE = {
    "job_description": "Backend Engineer, Platform. You will own Python services that sit in front of third-party model providers. Requirements: 2+ years production Python, strong async fundamentals.",
    "experience_notes": "Two years at a logistics startup. Built and owned a FastAPI service that wrapped a carrier rate API - handled retries, timeouts and their flaky rate limits.",
}


@pytest.fixture(autouse=True)
def _no_sleeping(monkeypatch):
    monkeypatch.setattr(MockProvider, "latency", 0)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample():
    return dict(SAMPLE)


@pytest.fixture
def debug_on(monkeypatch):
    """Dev-mode: APP_DEBUG=true. The settings object is cached, so reset it."""
    monkeypatch.setenv("APP_DEBUG", "true")
    get_settings.cache_clear()
    yield
    monkeypatch.delenv("APP_DEBUG", raising=False)
    get_settings.cache_clear()
