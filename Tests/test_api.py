import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.deps import get_db
from app.external_client import ExternalAPIError
from app.models import Post
from fastapi.testclient import TestClient

# Test DB
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def clear_db():
    db = TestingSessionLocal()
    db.query(Post).delete()
    db.commit()
    db.close()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_post_success(client):
    mock_data = {"id": 1, "title": "Test Title", "body": "Test Body"}
    with patch("app.external_client.fetch_external_post", new_callable=AsyncMock, return_value=mock_data):
        response = client.post("/posts/", json={"external_post_id": 1})
        assert response.status_code == 201
        data = response.json()
        assert data["external_id"] == 1
        assert data["title"] == "Test Title"

def test_create_post_external_not_found(client):
    with patch("app.external_client.fetch_external_post", new_callable=AsyncMock, side_effect=ExternalAPIError("Post not found on external API")):
        response = client.post("/posts/", json={"external_post_id": 999})
        assert response.status_code == 502

def test_get_post_success(client):
    mock_data = {"id": 2, "title": "Title", "body": "Body"}
    with patch("app.external_client.fetch_external_post", new_callable=AsyncMock, return_value=mock_data):
        client.post("/posts/", json={"external_post_id": 2})
    response = client.get("/posts/1")
    assert response.status_code == 200

def test_get_post_not_found(client):
    response = client.get("/posts/999")
    assert response.status_code == 404

def test_update_post_success(client):
    mock_data = {"id": 3, "title": "Title", "body": "Body"}
    with patch("app.external_client.fetch_external_post", new_callable=AsyncMock, return_value=mock_data):
        client.post("/posts/", json={"external_post_id": 3})
    response = client.put("/posts/1", json={"title": "Updated Title"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"

def test_update_post_not_found(client):
    response = client.put("/posts/999", json={"title": "Title"})
    assert response.status_code == 404

def test_delete_post_success(client):
    mock_data = {"id": 4, "title": "Title", "body": "Body"}
    with patch("app.external_client.fetch_external_post", new_callable=AsyncMock, return_value=mock_data):
        client.post("/posts/", json={"external_post_id": 4})
    response = client.delete("/posts/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Post deleted"}

def test_delete_post_not_found(client):
    response = client.delete("/posts/999")
    assert response.status_code == 404
