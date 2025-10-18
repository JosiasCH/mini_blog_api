# 📝 Mini Blog API

**API REST asíncrona** construida con **FastAPI**, **SQLAlchemy 2.0 (Async)**, **PostgreSQL**, Alembic, Pytest y Poetry.

Este proyecto fue diseñado para la Prueba Técnica Integral de Sintad S.A.C., con un enfoque riguroso en la **calidad del código**, el **testeo**, las **migraciones de base de datos** y la **contenerización vía Docker**.

---

## 📚 Índice

- [🧩 Fase 1 – Diseño y Modelado de la Base de Datos](#fase-1--diseño-y-modelado-de-la-base-de-datos)
- [🌸 Fase 2 – Configuración y Desarrollo del Backend](#fase-2--configuración-y-desarrollo-del-backend)
- [🧪 Fase 3 – Calidad de Código y Pruebas](#fase-3--calidad-de-código-y-pruebas)
- [🐳 Fase 4 – Documentación y Despliegue](#fase-4--documentación-y-despliegue)
- [🤖 Fase 5 – Prompt para Asistente de IA](#fase-5--prompt-para-asistente-de-ia)
- [📜 Autoría](#autoría)

---

## 🧩 Fase 1 – Diseño y Modelado de la Base de Datos

### 🧠 Descripción general

La base de datos utiliza **PostgreSQL** y sigue el estándar de la **Tercera Forma Normal (3NF)**, con integridad referencial estricta entre `users`, `posts` y `comments`.

### 🗺️ Diagrama Entidad-Relación (ERD)

<p align="center">
  <img src="docs/Mini-Blog-DB.png" alt="Mini Blog ERD" width="720">
</p>

### ⚙️ Elección de la Base de Datos (PostgreSQL)

Se eligió **PostgreSQL** por su **robustez ACID**, soporte para tipos de datos avanzados y su excelente integración nativa con **SQLAlchemy Async** y **Alembic**.

### 🧾 Estructura de Tablas

| Tabla | Campo | Tipo | Restricciones |
| :--- | :--- | :--- | :--- |
| **users** | `id` | `BIGSERIAL` | **PK** |
| | `username` | `VARCHAR(30)` | **UNIQUE**, **NOT NULL** |
| | `email` | `VARCHAR(254)` | **UNIQUE**, **NOT NULL** |
| | `password_hash` | `TEXT` | **NOT NULL** |
| | `created_at` | `TIMESTAMPTZ` | `DEFAULT now()`, **NOT NULL** |
| **posts** | `id` | `BIGSERIAL` | **PK** |
| | `title` | `VARCHAR(200)` | **NOT NULL** |
| | `content` | `TEXT` | **NOT NULL** |
| | `author_id` | `BIGINT` | **FK** → `users.id` (**ON DELETE RESTRICT**) |
| | `created_at` | `TIMESTAMPTZ` | `DEFAULT now()`, **NOT NULL** |
| **comments** | `id` | `BIGSERIAL` | **PK** |
| | `text` | `TEXT` | **NOT NULL** |
| | `post_id` | `BIGINT` | **FK** → `posts.id` (**ON DELETE CASCADE**) |
| | `author_id` | `BIGINT` | **FK** → `users.id` (**ON DELETE RESTRICT**) |
| | `created_at` | `TIMESTAMPTZ` | `DEFAULT now()`, **NOT NULL** |

---

## 🌸 Fase 2 – Configuración y Desarrollo del Backend

### 🧠 Descripción general

Stack moderno asincrónico con FastAPI y SQLAlchemy Async. Arquitectura modular con **separación de responsabilidades** (SoC) entre las capas de *Routing*, *Services/Business Logic*, *Schemas* y *Models*.

### ⚙️ Tecnologías principales

Python 3.10 · **FastAPI** · **SQLAlchemy 2.0 (Async)** · **Pydantic v2** · Alembic · Poetry · Uvicorn

### 🗂️ Estructura del proyecto

```bash
.
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── migrations/
│   └── versions/
├── envs/
│   ├── .env.example
│   └── .env.docker.example
├── src/mini_blog_api/
│   ├── main.py
│   ├── core/                  # Configuración (database, settings)
│   ├── models/                # Modelos SQLAlchemy ORM
│   │   └── models.py
│   ├── schemas/               # Modelos Pydantic
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── comments.py
│   ├── services/            # Capa de Negocio / CRUD
│   │   ├── users.py
│   │   ├── posts.py
│   │   └── comments.py
│   └── routers/               # Definición de Endpoints HTTP
│       ├── users.py
│       ├── posts.py
│       └── comments.py
└── tests/                   # Pruebas de Integración
    ├── conftest.py
    ├── test_users.py
    ├── test_posts.py
    └── test_comments.py