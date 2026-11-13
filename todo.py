import argparse
import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)


def add_task(title):
    tasks = load_tasks()
    tasks.append({"title": title, "done": False})
    save_tasks(tasks)
    print(f"Task added: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for number, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"{number}. [{mark}] {task['title']}")


def mark_done(number):
    tasks = load_tasks()
    if not 1 <= number <= len(tasks):
        print("Invalid task number.")
        return
    tasks[number - 1]["done"] = True
    save_tasks(tasks)
    print(f"Task {number} marked as done.")


def delete_task(number):
    tasks = load_tasks()
    if not 1 <= number <= len(tasks):
        print("Invalid task number.")
        return
    removed = tasks.pop(number - 1)
    save_tasks(tasks)
    print(f"Task deleted: {removed['title']}")


def main():
    parser = argparse.ArgumentParser(description="Simple Todo app")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("title")

    sub.add_parser("list", help="Show all tasks")

    p_done = sub.add_parser("done", help="Mark a task as done")
    p_done.add_argument("number", type=int)

    p_del = sub.add_parser("delete", help="Delete a task")
    p_del.add_argument("number", type=int)

    args = parser.parse_args()

    if args.command == "add":
        add_task(args.title)
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.number)
    elif args.command == "delete":
        delete_task(args.number)


if __name__ == "__main__":
    main()
