import argparse

from taskpilot import storage


def add_task(title, priority="medium", due=None):
    tasks = storage.load()
    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "done": False,
        "priority": priority,
        "due": due,
    }
    tasks.append(task)
    storage.save(tasks)
    return task

def list_tasks():
    return storage.load()

def complete_task(task_id):
    tasks = storage.load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            storage.save(tasks)
            return True
    return False


def delete_task(task_id):
    tasks = storage.load()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        return False
    storage.save(remaining)
    return True

def build_parser():
    parser = argparse.ArgumentParser(prog="taskpilot")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")

    p_add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    p_add.add_argument("--due", help="Due date, YYYY-MM-DD")

    sub.add_parser("list", help="Show all tasks")
    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("id", type=int)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("id", type=int)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "add":
        task = add_task(args.title, args.priority, args.due)
        print(f"Added #{task['id']}: {task['title']}")
        
    elif args.command == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks yet.")
        for t in tasks:
            mark = "x" if t["done"] else " "
            due = f" (due {t['due']})" if t.get("due") else ""
            print(f"[{mark}] #{t['id']} [{t.get('priority', 'medium')}] {t['title']}{due}")

    elif args.command == "done":
        print("Done!" if complete_task(args.id) else "Task not found.")
    elif args.command == "delete":
        print("Deleted." if delete_task(args.id) else "Task not found.")


if __name__ == "__main__":
    main()