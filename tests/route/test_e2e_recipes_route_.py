import pytest

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.database.models import User
import src.service.auth as auth_service

@pytest.mark.asyncio
async def test_create_recipe(client: TestClient, session: Session):
    # setting up user
    user = User(email='test@gmail.com', password='password', active=True)
    session.add(user)
    session.commit()

    access_token = await auth_service.create_token({'sub': user.email})

    recipe_json = {
        "title": "string",
        "description": "string",
        "instructions": "string",
        "ingredients": []
    }
    response = client.post(
        '/api/recipes',
        json=recipe_json,
        headers={"Authorization": f"Bearer {access_token}"}
        )
    assert response.status_code == 200
    # assert response.status_code == 300

    # client.get
    # client.put