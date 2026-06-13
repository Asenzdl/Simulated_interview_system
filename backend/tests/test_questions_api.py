import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database import Base, get_db
from src.main import app

# ── fixtures ────────────────────────────────────────────

engine = create_async_engine("sqlite+aiosqlite:///:memory:")
session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_db():
    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


# ── tests ───────────────────────────────────────────────

async def test_create_and_get(client: AsyncClient):
    resp = await client.post("/api/questions/", json={
        "title": "什么是闭包？",
        "content": "请解释",
        "difficulty": 3,
        "tags": ["JS", "闭包"],
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "什么是闭包？"
    assert len(data["tags"]) == 2
    qid = data["id"]

    resp = await client.get(f"/api/questions/{qid}")
    assert resp.status_code == 200
    assert resp.json()["id"] == qid


async def test_list_empty(client: AsyncClient):
    resp = await client.get("/api/questions/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 0
    assert data["items"] == []


async def test_list_pagination(client: AsyncClient):
    for i in range(5):
        await client.post("/api/questions/", json={"title": f"Q{i}"})

    resp = await client.get("/api/questions/", params={"page": 1, "page_size": 2})
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["pages"] == 3


async def test_update(client: AsyncClient):
    resp = await client.post("/api/questions/", json={"title": "原始"})
    qid = resp.json()["id"]

    resp = await client.put(f"/api/questions/{qid}", json={"title": "修改后", "difficulty": 5})
    assert resp.status_code == 200
    assert resp.json()["title"] == "修改后"
    assert resp.json()["difficulty"] == 5


async def test_delete(client: AsyncClient):
    resp = await client.post("/api/questions/", json={"title": "要删除"})
    qid = resp.json()["id"]

    resp = await client.delete(f"/api/questions/{qid}")
    assert resp.status_code == 204

    resp = await client.get(f"/api/questions/{qid}")
    assert resp.status_code == 404


async def test_get_not_found(client: AsyncClient):
    resp = await client.get("/api/questions/9999")
    assert resp.status_code == 404
