import argparse

from taskpilot import storage


def add_task(title):
    tasks = storage.load()
    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "done": False,
    }
    tasks.append(task)
    storage.save(tasks)
    return task

def list_tasks():
    return storage.load()

def build_parser():
    parser = argparse.ArgumentParser(prog="taskpilot")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")
    sub.add_parser("list", help="Show all tasks")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "add":
        task = add_task(args.title)
        print(f"Added #{task['id']}: {task['title']}")
        
    elif args.command == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks yet.")
        for t in tasks:
            mark = "x" if t["done"] else " "
            print(f"[{mark}] #{t['id']} {t['title']}")


if __name__ == "__main__":
    main()