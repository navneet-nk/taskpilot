import json
import os
from pathlib import Path


def db_path():
    return Path(os.environ.get("TASKPILOT_DB", Path.home() / ".taskpilot.json"))


def load():
    path = db_path()
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save(tasks):
    db_path().write_text(json.dumps(tasks, indent=2))