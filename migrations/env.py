from __future__ import annotations
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from alembic import context

# === 🔧 Agregar "src" al PYTHONPATH ===
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]  # raíz del repo
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

# === 📦 Importar Base, settings y MODELOS ===
from mini_blog_api.core.database import Base  # Base.metadata
from mini_blog_api.core.settings import settings
from mini_blog_api import models  # ← registra las tablas en Base.metadata

# === ⚙️ Configuración Alembic ===
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# === 🧱 Migraciones OFFLINE (solo genera SQL) ===
def run_migrations_offline() -> None:
    """Ejecuta migraciones sin conexión activa (solo genera SQL)."""
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# === ⚙️ Migraciones ONLINE (con conexión activa) ===
def do_run_migrations(connection: Connection) -> None:
    """Ejecuta migraciones con conexión activa."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # ✅ detecta cambios en tipo de columnas
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Crea el motor async y ejecuta las migraciones."""
    connectable = create_async_engine(settings.database_url, poolclass=pool.NullPool)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations() -> None:
    """Detecta si se ejecuta en modo offline u online."""
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        import asyncio
        asyncio.run(run_migrations_online())


# === 🚀 Punto de entrada ===
run_migrations()
