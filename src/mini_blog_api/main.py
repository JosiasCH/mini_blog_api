# src/mini_blog_api/main.py
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mini_blog_api.routers import users, posts, comments
from mini_blog_api.core.database import engine, Base


# ✅ Contexto de ciclo de vida moderno (lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Inicialización y limpieza de recursos al inicio/cierre de la app."""
    if os.getenv("RUN_STARTUP_DDL", "1") == "1":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas verificadas o creadas correctamente.")

    # La app corre aquí (yield = ciclo de vida activo)
    yield

    await engine.dispose()
    print("🛑 Conexión a la base de datos cerrada limpiamente.")


# ✅ Configuración principal de la aplicación FastAPI
app = FastAPI(
    title="Mini Blog API",
    version="1.0.0",
    description=(
        "Backend asíncrono para un sistema de mini-blog desarrollado "
        "como parte de la prueba técnica de Sintad S.A.C. "
        "Incluye gestión de usuarios, publicaciones y comentarios, "
        "implementado con FastAPI, SQLAlchemy Async y PostgreSQL."
    ),
    contact={
        "name": "Josías Chávez",
        "email": "josiaschavez@example.com",  # opcional
    },
    license_info={
        "name": "MIT License",
    },
    lifespan=lifespan,  # 👈 Usamos el manejador moderno
)


# ✅ Registro de routers (modular)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


# ✅ Punto de entrada opcional para ejecución directa
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mini_blog_api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
