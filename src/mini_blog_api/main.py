# src/mini_blog_api/main.py
import os
from fastapi import FastAPI
from mini_blog_api.routers import users, posts, comments

app = FastAPI(title="Mini Blog API")

# ❗️Sin prefix aquí — los routers ya lo traen internamente
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)

# Solo crear tablas en arranque si NO estamos en tests
if os.getenv("RUN_STARTUP_DDL", "1") == "1":
    from mini_blog_api.core.database import engine, Base

    @app.on_event("startup")
    async def on_startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
