FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PATH="/root/.local/bin:$PATH"

# paquetes base
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl libpq-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# copiar manifiestos antes para cache
COPY pyproject.toml poetry.lock* /app/

# instalar dependencias (sin el paquete)
RUN poetry install --no-root --only main

# copiar código y migraciones
COPY src /app/src
COPY alembic.ini /app/
COPY migrations /app/migrations

# variables por defecto (compose las sobreescribe)
ENV PYTHONPATH=/app/src \
    RUN_STARTUP_DDL=0 \
    DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/mini_blog

EXPOSE 8000

# migra y corre uvicorn
CMD ["bash", "-lc", "alembic upgrade head && uvicorn mini_blog_api.main:app --host 0.0.0.0 --port 8000"]
