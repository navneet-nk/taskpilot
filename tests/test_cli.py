import pytest

from taskpilot import cli


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    # Har test ke liye alag temporary database, aapka asli data safe rehta hai
    monkeypatch.setenv("TASKPILOT_DB", str(tmp_path / "db.json"))


def test_add_and_list():
    cli.add_task("Write code")
    assert [t["title"] for t in cli.list_tasks()] == ["Write code"]


def test_complete_task():
    t = cli.add_task("Test me")
    assert cli.complete_task(t["id"]) is True
    assert cli.list_tasks(status="done")[0]["id"] == t["id"]


def test_delete_missing_returns_false():
    assert cli.delete_task(999) is False


def test_search_and_priority_order():
    cli.add_task("Buy milk", priority="low")
    cli.add_task("Fix bug", priority="high")
    assert cli.list_tasks()[0]["title"] == "Fix bug"
    assert len(cli.list_tasks(search="milk")) == 1