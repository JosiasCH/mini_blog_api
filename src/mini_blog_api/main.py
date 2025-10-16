from fastapi import FastAPI
from mini_blog_api.core.database import engine, Base
from mini_blog_api.routers import users, posts, comments

app = FastAPI(title="Mini-Blog API", version="0.1.0")

@app.on_event("startup")
async def on_startup():
    # Solo para desarrollo; en Fase 3 usaremos Alembic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
