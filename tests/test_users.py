import pytest

@pytest.mark.asyncio
async def test_create_user_and_get(client):
    r = await client.post("/users/", json={
        "username": "alice",
        "email": "alice@mail.com",
        "password": "secret123"
    })
    assert r.status_code == 201
    data = r.json()
    assert "id" in data and data["username"] == "alice"

    r2 = await client.get(f"/users/{data['id']}")
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["username"] == "alice"
    assert data2["email"] == "alice@mail.com"

@pytest.mark.asyncio
async def test_create_user_conflict(client):
    # primer usuario OK
    await client.post("/users/", json={
        "username": "bob",
        "email": "bob@mail.com",
        "password": "secret123"
    })
    # duplicado (username/email)
    r = await client.post("/users/", json={
        "username": "bob",
        "email": "bob@mail.com",
        "password": "secret123"
    })
    assert r.status_code in (409, 400)
