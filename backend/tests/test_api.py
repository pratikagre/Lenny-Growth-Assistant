import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.database import init_db

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    await init_db()

@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Test SPA / web interface serving
        resp = await client.get("/")
        assert resp.status_code == 200
        # Test API metadata endpoint
        info_resp = await client.get("/api/info")
        assert info_resp.status_code == 200
        data = info_resp.json()
        assert data["status"] == "online"
        assert "version" in data

@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/api/health")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert data["database"]["status"] == "connected"
        assert data["vector_index"]["chunks_indexed"] > 0

@pytest.mark.asyncio
async def test_session_lifecycle():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Create Session
        create_resp = await client.post("/api/sessions", json={"title": "Test Strategy Session"})
        assert create_resp.status_code == 201
        session_data = create_resp.json()
        session_id = session_data["id"]
        assert session_data["title"] == "Test Strategy Session"

        # 2. List Sessions
        list_resp = await client.get("/api/sessions")
        assert list_resp.status_code == 200
        sessions = list_resp.json()
        assert any(s["id"] == session_id for s in sessions)

        # 3. Get Session Detail
        detail_resp = await client.get(f"/api/sessions/{session_id}")
        assert detail_resp.status_code == 200
        detail = detail_resp.json()
        assert detail["id"] == session_id
        assert "messages" in detail
        assert "artifacts" in detail

        # 4. Delete Session
        del_resp = await client.delete(f"/api/sessions/{session_id}")
        assert del_resp.status_code == 204

        # 5. Verify deleted
        get_after_del = await client.get(f"/api/sessions/{session_id}")
        assert get_after_del.status_code == 404
