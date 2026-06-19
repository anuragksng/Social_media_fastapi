from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json())
    assert res.json().get('message') == 'Home Page'


def test_create_user():
    res = client.post("/users/", json={"email": "anu@gmail.com", "password": "passqord123"})
    print(res.json())
    assert res.status_code == 201