import argparse

from taskpilot import storage


def add_task(title, priority="medium", due=None, user_id=None):
    return storage.insert(title, priority, due, user_id)


def list_tasks(status=None, search=None, user_id=None):
    tasks = storage.get_all(user_id)
    if status == "done":
        tasks = [t for t in tasks if t["done"]]
    elif status == "pending":
        tasks = [t for t in tasks if not t["done"]]
    if search:
        tasks = [t for t in tasks if search.lower() in t["title"].lower()]
    order = {"high": 0, "medium": 1, "low": 2}
    return sorted(tasks, key=lambda t: order.get(t.get("priority", "medium"), 1))

def complete_task(task_id, user_id=None):
    return storage.mark_done(task_id, user_id)


def delete_task(task_id, user_id=None):
    return storage.delete(task_id, user_id)

def build_parser():
    parser = argparse.ArgumentParser(prog="taskpilot")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")

    p_add.add_argument("--priority", choices=["low", "medium", "high"], default="medium")
    p_add.add_argument("--due", help="Due date, YYYY-MM-DD")

    p_list = sub.add_parser("list", help="Show tasks")
    p_list.add_argument("--status", choices=["done", "pending"])
    p_list.add_argument("--search")

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
        tasks = list_tasks(args.status, args.search)
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