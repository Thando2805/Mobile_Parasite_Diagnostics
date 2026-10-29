import io
from fastapi.testclient import TestClient
from PIL import Image
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_invalid_file_upload():
    # Sending a text file instead of an image should trigger a 400 Bad Request
    response = client.post(
        "/api/v1/predict",
        files={"file": ("test.txt", b"hello world", "text/plain")}
    )
    assert response.status_code == 400
    assert "detail" in response.json()