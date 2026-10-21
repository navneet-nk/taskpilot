import pytest
from fastapi.testclient import TestClient

from taskpilot.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKPILOT_DB", str(tmp_path / "test.db"))


def auth_headers(username="alice"):
    r = client.post("/register", json={"username": username, "password": "secret123"})
    return {"Authorization": "Bearer " + r.json()["token"]}


def test_create_and_list():
    h = auth_headers()
    r = client.post("/tasks", json={"title": "Write API", "priority": "high"}, headers=h)
    assert r.status_code == 201
    assert client.get("/tasks", headers=h).json()[0]["title"] == "Write API"


def test_toggle_done():
    h = auth_headers()
    t = client.post("/tasks", json={"title": "Check me"}, headers=h).json()
    r = client.patch(f"/tasks/{t['id']}", json={"done": True}, headers=h)
    assert r.status_code == 200
    assert client.get("/tasks?status=done", headers=h).json()[0]["id"] == t["id"]


def test_delete_missing_returns_404():
    assert client.delete("/tasks/999", headers=auth_headers()).status_code == 404


def test_tasks_require_login():
    assert client.get("/tasks").status_code == 401


def test_users_cannot_see_each_others_tasks():
    alice = auth_headers("alice")
    bob = auth_headers("bobby")
    t = client.post("/tasks", json={"title": "Private"}, headers=alice).json()
    assert client.get("/tasks", headers=bob).json() == []
    assert client.delete(f"/tasks/{t['id']}", headers=bob).status_code == 404