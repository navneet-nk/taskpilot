import pytest
from fastapi.testclient import TestClient

from taskpilot import auth
from taskpilot.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKPILOT_DB", str(tmp_path / "test.db"))


def test_password_hash_roundtrip():
    h = auth.hash_password("secret123")
    assert h != "secret123"
    assert auth.verify_password("secret123", h)
    assert not auth.verify_password("wrong", h)


def test_register_and_login():
    r = client.post("/register", json={"username": "Alice", "password": "secret123"})
    assert r.status_code == 201 and "token" in r.json()
    r = client.post("/login", json={"username": "alice", "password": "secret123"})
    assert r.status_code == 200


def test_duplicate_register_returns_409():
    body = {"username": "bob", "password": "secret123"}
    client.post("/register", json=body)
    assert client.post("/register", json=body).status_code == 409


def test_wrong_password_returns_401():
    client.post("/register", json={"username": "carol", "password": "secret123"})
    r = client.post("/login", json={"username": "carol", "password": "nope-nope"})
    assert r.status_code == 401