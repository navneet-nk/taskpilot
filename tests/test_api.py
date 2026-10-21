import pytest
from fastapi.testclient import TestClient

from taskpilot.api import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    monkeypatch.setenv("TASKPILOT_DB", str(tmp_path / "test.db"))


def test_create_and_list():
    r = client.post("/tasks", json={"title": "Write API", "priority": "high"})
    assert r.status_code == 201
    assert client.get("/tasks").json()[0]["title"] == "Write API"


def test_toggle_done():
    t = client.post("/tasks", json={"title": "Check me"}).json()
    r = client.patch(f"/tasks/{t['id']}", json={"done": True})
    assert r.status_code == 200
    assert client.get("/tasks?status=done").json()[0]["id"] == t["id"]


def test_delete_missing_returns_404():
    assert client.delete("/tasks/999").status_code == 404