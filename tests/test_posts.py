import pytest

@pytest.mark.asyncio
async def test_list_and_get_post(client):
    # crea usuario
    u = await client.post("/users/", json={
        "username":"carlos", "email":"carlos@mail.com", "password":"secret123"
    })
    assert u.status_code == 201
    uid = u.json()["id"]

    # lista vacía
    r0 = await client.get("/posts/?limit=5")
    assert r0.status_code == 200
    assert r0.json() == []

    # crea post
    p = await client.post("/posts/", json={
        "title":"Hola", "content":"Mundo", "author_id": uid
    })
    assert p.status_code == 201
    pid = p.json()["id"]

    # lista con 1
    r1 = await client.get("/posts/?limit=5")
    assert r1.status_code == 200
    assert len(r1.json()) == 1

    # get by id
    r2 = await client.get(f"/posts/{pid}")
    assert r2.status_code == 200
    data = r2.json()
    assert data["title"] == "Hola"
    assert data["comments"] == []

    # agrega comentario
    c = await client.post(f"/posts/{pid}/comments", json={
        "text": "¡Buen post!",
        "author_id": uid
    })
    assert c.status_code in (201, 200)  # según tu implementación

    # get by id con comentario
    r3 = await client.get(f"/posts/{pid}")
    assert r3.status_code == 200
    data3 = r3.json()
    assert len(data3["comments"]) == 1
    assert data3["comments"][0]["text"] == "¡Buen post!"
