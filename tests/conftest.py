# tests/conftest.py
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text  # 👈 necesario para ejecutar SQL literal
from httpx import AsyncClient, ASGITransport

# --- Forzamos URL de test y desactivamos DDL en startup de la app ---
os.environ["TEST_DATABASE_URL"] = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:josiitas123@localhost:5432/mini_blog_test",
)
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]
os.environ["RUN_STARTUP_DDL"] = "0"

from mini_blog_api.main import app
from mini_blog_api.core.database import Base, get_session


@pytest.fixture(scope="session")
def anyio_backend():
    """Asegura backend asyncio para pytest-anyio/pytest-asyncio."""
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    """
    Engine de tests creado una vez por sesión.
    NullPool evita reusar conexiones (mitiga issues en Windows).
    """
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        future=True,
        poolclass=NullPool,
    )
    try:
        # Crear todas las tablas una sola vez
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(autouse=True)
async def _db_clean(engine):
    """
    Limpia la BD antes de CADA test para aislarlos:
    TRUNCATE + RESTART IDENTITY + CASCADE.
    """
    async with engine.begin() as conn:
        await conn.execute(
            text("TRUNCATE TABLE comments, posts, users RESTART IDENTITY CASCADE;")
        )
    yield


@pytest.fixture
async def session_factory(engine):
    """Fábrica de sesiones para inyectar en la app (una por request)."""
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def client(session_factory):
    """
    Cliente HTTP asíncrono con override de la dependencia get_session.
    Usamos ASGITransport (httpx moderno) y NO ejecutamos lifespan.
    """
    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
