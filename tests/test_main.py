import os
import uuid
from pathlib import Path
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from app.models.entities import User, Book
from app.auth.auth_handler import get_password_hash
from app.db.database import init_db, session_context
from app.main import app

_test_db_name = f"test_{uuid.uuid4().hex}.db"
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{_test_db_name}"


@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_db():
    db_path = Path(_test_db_name)
    await init_db()
    async with session_context() as session:
        user = User(
            username="testuser",
            hashed_password=get_password_hash("testpass"),
        )
        session.add(user)
        await session.commit()
    yield
    async with session_context() as session:
        await session.execute(delete(Book))
        await session.execute(delete(User))
        await session.commit()
    if db_path.exists():
        db_path.unlink()


@pytest.mark.asyncio
async def test_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/token",
            data={"username": "testuser", "password": "testpass"},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_create_book():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post(
            "/token",
            data={"username": "testuser", "password": "testpass"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.post(
            "/books/",
            json={"title": "Book1", "author": "Author1"},
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Book1"


@pytest.mark.asyncio
async def test_read_books():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        login = await ac.post(
            "/token",
            data={"username": "testuser", "password": "testpass"},
        )
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        response = await ac.get("/books/", headers=headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
