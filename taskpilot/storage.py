import os
import sqlite3
from contextlib import closing
from pathlib import Path


def db_path():
    return Path(os.environ.get("TASKPILOT_DB", Path.home() / ".taskpilot.db"))


def connect():
    conn = sqlite3.connect(db_path())
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            priority TEXT NOT NULL DEFAULT 'medium',
            due TEXT
        )
        """
    )
    return conn


def _to_dict(row):
    task = dict(row)
    task["done"] = bool(task["done"])
    return task


def get_all():
    with closing(connect()) as conn:
        rows = conn.execute("SELECT * FROM tasks").fetchall()
    return [_to_dict(r) for r in rows]


def insert(title, priority, due):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, priority, due) VALUES (?, ?, ?)",
                (title, priority, due),
            )
        task_id = cur.lastrowid
    return {"id": task_id, "title": title, "done": False, "priority": priority, "due": due}


def mark_done(task_id):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        return cur.rowcount > 0

def set_done(task_id, done):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute(
                "UPDATE tasks SET done = ? WHERE id = ?", (int(done), task_id)
            )
        return cur.rowcount > 0
    
def delete(task_id):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cur.rowcount > 0