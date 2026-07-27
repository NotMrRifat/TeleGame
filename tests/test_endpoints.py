"""Unit tests for FastAPI endpoints and Vercel serverless gateway."""

import pytest
from httpx import ASGITransport, AsyncClient

from api.index import app as vercel_app
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test / endpoint metadata."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert data["app"] == "TeleGame"


@pytest.mark.asyncio
async def test_health_endpoint():
    """Test /health liveness check."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data


@pytest.mark.asyncio
async def test_metrics_endpoint():
    """Test /metrics telemetry endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "loaded_games_count" in data
    assert "available_plugins" in data


@pytest.mark.asyncio
async def test_readiness_endpoint():
    """Test /readiness database check."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/readiness")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.asyncio
async def test_cron_cleanup_endpoint():
    """Test /api/cron/cleanup serverless cron."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/cron/cleanup")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_vercel_asgi_export():
    """Verify Vercel ASGI app is exported correctly."""
    assert vercel_app is app
