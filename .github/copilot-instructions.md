
## Mini Blog API — Instrucciones para Agentes de IA (Meta-prompt)

Actúa como un desarrollador backend senior experto en Python, FastAPI, SQLAlchemy Async y Pydantic v2. Prioriza calidad, legibilidad, tipado y pruebas. Explica decisiones breves cuando aporten claridad.

1) Contexto del proyecto
- Stack: Python 3.10, FastAPI (APIRouter + lifespan), SQLAlchemy 2.0 async, Pydantic v2, Alembic, pytest (async), Poetry.
- Estructura: `src/mini_blog_api/` con `core/`, `models/`, `schemas/`, `routers/` y `main.py` como entrypoint.
- Ciclo de vida: `main.py` usa `lifespan`. `RUN_STARTUP_DDL` controla creación automática de tablas (setear a `0` en tests).

2) Principios y reglas obligatorias
- SOLID/DRY/KISS: funciones cortas y cohesionadas; mover lógica compleja a `services/` o `crud/` si es necesario.
- Tipado exhaustivo en firmas y modelos; docstrings concisos si aportan claridad.
- No exponer credenciales ni `password_hash` en responses o logs.
- Maneja códigos HTTP: 201 creación, 200 OK, 404 not found, 409 conflict (unicidad), 400 validación.

3) Conveciones FastAPI / DB
- Routers: siempre `APIRouter(prefix=..., tags=[...])` y `response_model=...` cuando devuelvas entidades.
- Inyectar sesión con `Depends(get_session)` (AsyncSession) desde `src/mini_blog_api/core/database.py`.
- Evitar N+1: al devolver relaciones usar `select(...).options(selectinload(...))` (ej. `routers/posts.py`).
- Transacciones: `session.add(...)` -> `await session.commit()` -> `await session.refresh(obj)` o recarga con `select` + `selectinload`.
- Integridad: al capturar `IntegrityError` hacer `await session.rollback()` y lanzar `HTTPException(status_code=409, detail=... )`.

4) Migraciones y despliegue
- Generar revisiones: `alembic revision --autogenerate -m "mensaje"` y revisar el diff antes de commitear.
- Aplicar migraciones: `alembic upgrade head`.
- `migrations/env.py` ya configura `compare_type=True`.

5) Pruebas (pytest)
- Ejecutar: `poetry run pytest -v`.
- Fixtures: `tests/conftest.py` crea engine (NullPool en Windows), session_factory y cliente HTTP con `ASGITransport`.
- Inyección test DB: `app.dependency_overrides[get_session]` sustituye la dependencia por la sesión de prueba.
- Aislamiento: `_db_clean` ejecuta `TRUNCATE TABLE comments, posts, users RESTART IDENTITY CASCADE;` antes de cada test.

6) Patrones concretos (extractos del repo)
- Crear usuario: usar `passlib.hash.bcrypt` y truncar password a 72 chars. Manejar `IntegrityError` -> rollback -> `HTTPException(409, "Usuario ya existe")` (`routers/users.py`).
- Crear post: validar FK con `await session.get(User, author_id)` -> 404 si no existe; `session.add()` -> `await session.commit()` -> recargar con `selectinload(Post.comments)` (`routers/posts.py`).
- Tests: usar `AsyncClient(transport=ASGITransport(app=app), base_url="http://test")` y override de `get_session` (`tests/conftest.py`).

7) Do's & Don'ts rápidos
- ✅ Usa AsyncSession y `await` en todas las operaciones DB.
- ✅ Define `response_model` y schemas Pydantic v2 con `model_config = ConfigDict(from_attributes=True)` para salidas.
- ✅ Evita N+1 con `selectinload` antes de serializar relaciones.
- ❌ No mezcles sync/async ni hagas operaciones bloqueantes en el loop.
- ❌ No expongas fields sensibles en responses ni logs.

Referencias rápidas (leer antes de programar):
- `src/mini_blog_api/main.py` — lifespan y registro de routers.
- `src/mini_blog_api/core/settings.py` — carga de envs; `TEST_DATABASE_URL` puede sobrescribir `DATABASE_URL`.
- `src/mini_blog_api/core/database.py` — engine, SessionLocal, `get_session`.
- `src/mini_blog_api/models/models.py` — mappings y `ondelete` en FKs.
- `src/mini_blog_api/routers/*.py` — ejemplos de endpoints con commit/refresh y `selectinload`.
- `tests/conftest.py` — fixtures y limpieza entre tests.

Si quieres, puedo:
- Generar una plantilla (router + schemas + tests) que siga exactamente estas reglas.
- Traducir o acortar este meta-prompt.

