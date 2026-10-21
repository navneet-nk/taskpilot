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
            due TEXT,
            user_id INTEGER
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        """
    )
    cols = [r["name"] for r in conn.execute("PRAGMA table_info(tasks)")]
    if "user_id" not in cols:
        conn.execute("ALTER TABLE tasks ADD COLUMN user_id INTEGER")
    return conn


def _to_dict(row):
    task = dict(row)
    task["done"] = bool(task["done"])
    task.pop("user_id", None)
    return task


# user_id=None ka matlab CLI wale tasks. "IS ?" NULL ke saath bhi kaam karta hai.
def get_all(user_id=None):
    with closing(connect()) as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE user_id IS ?", (user_id,)
        ).fetchall()
    return [_to_dict(r) for r in rows]


def insert(title, priority, due, user_id=None):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute(
                "INSERT INTO tasks (title, priority, due, user_id) VALUES (?, ?, ?, ?)",
                (title, priority, due, user_id),
            )
        task_id = cur.lastrowid
    return {"id": task_id, "title": title, "done": False, "priority": priority, "due": due}


def mark_done(task_id, user_id=None):
    return set_done(task_id, True, user_id)


def set_done(task_id, done, user_id=None):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute(
                "UPDATE tasks SET done = ? WHERE id = ? AND user_id IS ?",
                (int(done), task_id, user_id),
            )
        return cur.rowcount > 0


def delete(task_id, user_id=None):
    with closing(connect()) as conn:
        with conn:
            cur = conn.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id IS ?", (task_id, user_id)
            )
        return cur.rowcount > 0


def create_user(username, password_hash):
    with closing(connect()) as conn:
        try:
            with conn:
                cur = conn.execute(
                    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                    (username, password_hash),
                )
        except sqlite3.IntegrityError:
            return None
        return cur.lastrowid


def get_user(username):
    with closing(connect()) as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    return dict(row) if row else None