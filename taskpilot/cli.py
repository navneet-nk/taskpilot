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


def build_parser():
    parser = argparse.ArgumentParser(prog="taskpilot")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command == "add":
        task = add_task(args.title)
        print(f"Added #{task['id']}: {task['title']}")


if __name__ == "__main__":
    main()