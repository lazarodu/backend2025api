# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    # Registro
    response = await client.post("/users/register", json={
        "name": "Test",
        "email": "test@example.com",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User registered successfully"

    # Login
    response = await client.post("/users/login", data={
        "username": "test@example.com",
        "password": "test123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
