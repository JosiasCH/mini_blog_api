FROM python:3.10-slim

# Evita .pyc y stdout con buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Paquetes base
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

# Instalar Poetry (sin venvs)
ENV POETRY_VERSION=1.8.3 POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Manifiestos primero (mejor cache)
COPY pyproject.toml poetry.lock* ./

# Instala deps SIN instalar el paquete (evita exigir README)
# Asegura herramientas runtime y fija bcrypt<4 para passlib
RUN poetry lock --no-interaction && \
    poetry install --no-interaction --no-ansi --no-root && \
    pip install --no-cache-dir \
      alembic \
      asyncpg \
      "uvicorn[standard]" \
      fastapi \
      pydantic-settings \
      "pydantic[email]" \
      "SQLAlchemy>=2" \
      httpx \
      "passlib[bcrypt]==1.7.4" \
      "bcrypt==3.2.2"

# Código y migraciones
COPY src ./src
COPY alembic.ini .
COPY migrations ./migrations

# Valor por defecto (compose lo sobreescribe con env_file)
ENV DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/mini_blog

EXPOSE 8000

# Arranque: migraciones + uvicorn
CMD ["bash", "-lc", "poetry run alembic upgrade head && poetry run uvicorn mini_blog_api.main:app --host 0.0.0.0 --port 8000 --app-dir src"]
