
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager

load_dotenv()

# Permitir sobrescrever pelo ambiente (ex: testes)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    DATABASE_URL = (
        f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:"
        f"{os.getenv('POSTGRES_PASSWORD')}@"
        f"{POSTGRES_HOST}:5432/"
        f"{os.getenv('POSTGRES_DB')}"
    )

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        url = os.getenv("DATABASE_URL", DATABASE_URL)
        _engine = create_async_engine(url, echo=True, future=True)
    return _engine


def _get_session_factory():
    return sessionmaker(
        bind=get_engine(),
        class_=AsyncSession,
        expire_on_commit=False,
    )


async def init_db():
    async with get_engine().begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def session_context():
    """Context manager para uso manual.

    Uso: async with session_context() as session:
    """
    SessionLocal = _get_session_factory()
    async with SessionLocal() as session:  # type: ignore
        yield session


async def get_session():
    """Dependency para FastAPI (yield pattern)."""
    SessionLocal = _get_session_factory()
    async with SessionLocal() as session:  # type: ignore
        yield session
