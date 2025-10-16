# tests/conftest.py
import os
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
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
    """
    Usamos anyio/pytest-asyncio modo auto. Este fixture asegura backend compatible.
    """
    return "asyncio"


@pytest.fixture(scope="session")
async def engine():
    """
    Engine de tests creado una vez por sesión. NullPool evita reusar conexiones
    y mitiga 'another operation is in progress' en Windows.
    """
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        future=True,
        poolclass=NullPool,
    )
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="session", autouse=True)
async def setup_db(engine):
    """
    Crea todas las tablas antes de los tests y las elimina al final.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def session_factory(engine):
    """
    Fabrica de sesiones para inyectar en la app (una por request).
    """
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
async def client(session_factory):
    """
    Cliente HTTP asíncrono con override de la dependencia get_session.
    No usamos LifespanManager -> no ejecuta startup/shutdown.
    """
    async def override_get_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    transport = ASGITransport(app=app)  # httpx moderno (sin parámetro app en AsyncClient)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
