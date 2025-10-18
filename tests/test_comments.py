# tests/test_comments.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_add_comment(client: AsyncClient):
    # Crear usuario y post primero
    u = await client.post("/users/", json={"username": "carl", "email": "carl@example.com", "password": "secret123"})
    assert u.status_code == 201
    uid = u.json()["id"]

    p = await client.post("/posts/", json={"title": "Nuevo post", "content": "Contenido", "author_id": uid})
    assert p.status_code == 201
    pid = p.json()["id"]

    # Crear comentario
    payload = {"text": "Buen post!", "author_id": uid}
    response = await client.post(f"/posts/{pid}/comments/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["text"] == "Buen post!"
    assert data["author_id"] == uid

@pytest.mark.asyncio
async def test_list_comments(client: AsyncClient):
    # Prepara usuario y post
    u = await client.post("/users/", json={"username": "dani", "email": "dani@example.com", "password": "secret123"})
    uid = u.json()["id"]
    p = await client.post("/posts/", json={"title": "Otro post", "content": "Más contenido", "author_id": uid})
    pid = p.json()["id"]

    # Agrega un comentario
    await client.post(f"/posts/{pid}/comments/", json={"text":"Hola!", "author_id": uid})

    # Lista comentarios
    response = await client.get(f"/posts/{pid}/comments/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["text"] == "Hola!"
