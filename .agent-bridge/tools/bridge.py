#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry"
TASKS = REGISTRY / "tasks"
THREADS = ROOT / "threads"
INBOX = ROOT / "inbox"
ARCHIVE = ROOT / "archive"
STATE = ROOT / "state"
INDEX = REGISTRY / "index.json"
LOCKS = ROOT / "locks"
ROOT_NAME = ROOT.name


MESSAGE_TYPES = {
    "task_created",
    "status_update",
    "question",
    "answer",
    "review_request",
    "review_response",
    "changes_applied",
    "approval",
    "blocked",
    "stale_review_notice",
    "task_completed",
    "task_archived",
}

HEAD_COMMIT_MESSAGE_TYPES = {
    "task_created",
    "review_request",
    "changes_applied",
}


@dataclass
class Task:
    task_id: str
    data: dict[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    for path in [TASKS, THREADS, INBOX / "claude", INBOX / "codex", ARCHIVE, STATE, LOCKS]:
        path.mkdir(parents=True, exist_ok=True)
    if not INDEX.exists():
        atomic_write_json(INDEX, {"active_tasks": [], "archived_months": [], "completed_tasks": 0})


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(content)
        tmp.flush()
        os.fsync(tmp.fileno())
        temp_name = tmp.name
    os.replace(temp_name, path)


def atomic_write_json(path: Path, data: Any) -> None:
    atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def slugify(value: str) -> str:
    keep = []
    for ch in value.lower():
        keep.append(ch if ch.isalnum() else "-")
    text = "".join(keep)
    while "--" in text:
        text = text.replace("--", "-")
    return text.strip("-")[:40] or "task"


def allocate_task_id() -> str:
    date_part = datetime.now().strftime("%Y%m%d")
    existing = sorted(p.stem for p in TASKS.glob(f"TASK-{date_part}-*.json"))
    if not existing:
        seq = 1
    else:
        seq = max(int(name.split("-")[-1]) for name in existing) + 1
    return f"TASK-{date_part}-{seq:03d}"


class FileLock:
    def __init__(self, path: Path, timeout_seconds: float = 10.0, poll_seconds: float = 0.05):
        self.path = path
        self.timeout_seconds = timeout_seconds
        self.poll_seconds = poll_seconds
        self.fd: int | None = None

    def __enter__(self) -> "FileLock":
        deadline = time.monotonic() + self.timeout_seconds
        while True:
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
                os.write(self.fd, str(os.getpid()).encode("utf-8"))
                return self
            except FileExistsError:
                if time.monotonic() >= deadline:
                    raise SystemExit(f"Timed out waiting for lock: {self.path}")
                time.sleep(self.poll_seconds)

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def task_path(task_id: str) -> Path:
    return TASKS / f"{task_id}.json"


def load_task(task_id: str) -> Task:
    path = task_path(task_id)
    if not path.exists():
        raise SystemExit(f"Task not found: {task_id}")
    return Task(task_id=task_id, data=load_json(path))


def thread_dir(task_id: str) -> Path:
    return THREADS / task_id


def next_message_id(task_id: str) -> str:
    directory = thread_dir(task_id)
    directory.mkdir(parents=True, exist_ok=True)
    nums: list[int] = []
    for p in directory.glob("*.json"):
        if p.name == "SUMMARY.json":
            continue
        prefix = p.stem.split("-", 1)[0]
        if prefix.isdigit():
            nums.append(int(prefix))
    return f"{(max(nums) + 1 if nums else 1):04d}"


def update_index_active(task_id: str, *, remove: bool = False, archived_month: str | None = None) -> None:
    data = load_json(INDEX)
    active = set(data.get("active_tasks", []))
    if remove:
        active.discard(task_id)
    else:
        active.add(task_id)
    data["active_tasks"] = sorted(active)
    if archived_month:
        months = set(data.get("archived_months", []))
        months.add(archived_month)
        data["archived_months"] = sorted(months)
    atomic_write_json(INDEX, data)


def bump_state(agent: str, task_id: str, message_id: str, increment_unread: bool) -> None:
    path = STATE / f"{agent}.json"
    state = load_json(path) if path.exists() else {"agent": agent, "last_seen": {}, "open_tasks": [], "unread_count": 0}
    open_tasks = set(state.get("open_tasks", []))
    open_tasks.add(task_id)
    state["open_tasks"] = sorted(open_tasks)
    if increment_unread:
        state["unread_count"] = int(state.get("unread_count", 0)) + 1
    state.setdefault("last_seen", {})
    atomic_write_json(path, state)


def write_inbox_pointer(to_agent: str, message: dict[str, Any]) -> None:
    pointer = {
        "task_id": message["task_id"],
        "latest_message_id": message["message_id"],
        "latest_type": message["type"],
        "from": message["from"],
        "status": message["status"],
        "thread_path": f"{ROOT_NAME}/threads/{message['task_id']}",
        "summary": message["summary"],
        "created_at": message["created_at"],
    }
    atomic_write_json(INBOX / to_agent / f"{message['task_id']}.json", pointer)
    bump_state(to_agent, message["task_id"], message["message_id"], increment_unread=True)


def cmd_new_task(args: argparse.Namespace) -> None:
    ensure_dirs()
    with FileLock(LOCKS / "new-task.lock"):
        task_id = allocate_task_id()
        tdir = thread_dir(task_id)
        tdir.mkdir(parents=True, exist_ok=True)
        task = {
            "task_id": task_id,
            "title": args.title,
            "created_at": utc_now(),
            "created_by": args.created_by,
            "repo": args.repo,
            "branch": args.branch,
            "status": args.status,
            "assigned_to": args.assigned_to,
            "reviewer": args.reviewer,
            "thread_path": f"{ROOT_NAME}/threads/{task_id}",
            "latest_message_id": "0001",
            "latest_head_commit": args.head_commit,
            "archive_status": "active",
        }
        atomic_write_json(task_path(task_id), task)

        first_message = {
            "message_id": "0001",
            "task_id": task_id,
            "from": args.created_by,
            "to": args.assigned_to,
            "type": "task_created",
            "created_at": utc_now(),
            "in_reply_to": None,
            "summary": f"Task created: {args.title}",
            "body": {
                "title": args.title,
                "repo": args.repo,
                "branch": args.branch,
                "head_commit": args.head_commit,
                "notes": args.notes,
            },
            "status": "open",
        }
        atomic_write_json(tdir / "0001-task-created.json", first_message)
        update_index_active(task_id)
        write_inbox_pointer(args.assigned_to, first_message)
    print(task_id)


def read_body(body_file: str | None) -> dict[str, Any]:
    if not body_file:
        return {}
    with open(body_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, dict):
            raise SystemExit("body-file must contain a JSON object")
        return data


def cmd_send(args: argparse.Namespace) -> None:
    ensure_dirs()
    if args.type not in MESSAGE_TYPES:
        raise SystemExit(f"Unsupported message type: {args.type}")
    task = load_task(args.task)
    body = read_body(args.body_file)
    with FileLock(LOCKS / f"{args.task}.message.lock"):
        msg_id = next_message_id(args.task)
        message = {
            "message_id": msg_id,
            "task_id": args.task,
            "from": args.sender,
            "to": args.to,
            "type": args.type,
            "created_at": utc_now(),
            "in_reply_to": args.in_reply_to,
            "summary": args.summary,
            "body": body,
            "status": args.status,
        }
        filename = f"{msg_id}-{args.type.replace('_', '-')}.json"
        atomic_write_json(thread_dir(args.task) / filename, message)

        task.data["latest_message_id"] = msg_id
        if args.task_status:
            task.data["status"] = args.task_status
        if args.type in HEAD_COMMIT_MESSAGE_TYPES and isinstance(body.get("head_commit"), str):
            task.data["latest_head_commit"] = body["head_commit"]
        atomic_write_json(task_path(args.task), task.data)
        write_inbox_pointer(args.to, message)
    print(filename)


def cmd_inbox(args: argparse.Namespace) -> None:
    ensure_dirs()
    idir = INBOX / args.agent
    items = []
    for p in sorted(idir.glob("*.json")):
        items.append(load_json(p))
    print(json.dumps(items, indent=2))


def cmd_read(args: argparse.Namespace) -> None:
    ensure_dirs()
    tdir = thread_dir(args.task)
    if not tdir.exists():
        raise SystemExit(f"Thread not found: {args.task}")
    payload = {
        "task": load_task(args.task).data,
        "summary": load_json(tdir / "SUMMARY.json") if (tdir / "SUMMARY.json").exists() else None,
        "messages": [load_json(p) for p in sorted(tdir.glob("*.json")) if p.name != "SUMMARY.json"],
    }
    print(json.dumps(payload, indent=2))


def cmd_complete(args: argparse.Namespace) -> None:
    ensure_dirs()
    task = load_task(args.task)
    with FileLock(LOCKS / f"{args.task}.message.lock"):
        task.data["status"] = "completed"
        atomic_write_json(task_path(args.task), task.data)
        msg_id = next_message_id(args.task)
        message = {
            "message_id": msg_id,
            "task_id": args.task,
            "from": args.sender,
            "to": "human",
            "type": "task_completed",
            "created_at": utc_now(),
            "in_reply_to": None,
            "summary": "Task marked completed",
            "body": {},
            "status": "closed",
        }
        atomic_write_json(thread_dir(args.task) / f"{msg_id}-task-completed.json", message)
        task.data["latest_message_id"] = msg_id
        atomic_write_json(task_path(args.task), task.data)
    print(args.task)


def cmd_archive(args: argparse.Namespace) -> None:
    ensure_dirs()
    task = load_task(args.task)
    month = datetime.now().strftime("%Y-%m")
    destination = ARCHIVE / month / args.task
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(thread_dir(args.task)), str(destination))
    task.data["archive_status"] = "archived"
    task.data["thread_path"] = f"{ROOT_NAME}/archive/{month}/{args.task}"
    atomic_write_json(task_path(args.task), task.data)
    update_index_active(args.task, remove=True, archived_month=month)
    print(str(destination))


def cmd_summarize(args: argparse.Namespace) -> None:
    ensure_dirs()
    tdir = thread_dir(args.task)
    msgs = [load_json(p) for p in sorted(tdir.glob("*.json")) if p.name != "SUMMARY.json"]
    if not msgs:
        raise SystemExit("No messages found")
    summary = {
        "task_id": args.task,
        "current_status": load_task(args.task).data["status"],
        "latest_message_id": msgs[-1]["message_id"],
        "latest_head_commit": load_task(args.task).data.get("latest_head_commit"),
        "participants": sorted({m["from"] for m in msgs} | {m["to"] for m in msgs}),
        "recent_summaries": [m["summary"] for m in msgs[-5:]],
    }
    atomic_write_json(tdir / "SUMMARY.json", summary)
    print(str(tdir / "SUMMARY.json"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent bridge helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new-task")
    p.add_argument("--title", required=True)
    p.add_argument("--created-by", default="human")
    p.add_argument("--repo", default="inhouse")
    p.add_argument("--branch", default="main")
    p.add_argument("--assigned-to", choices=["claude", "codex"], required=True)
    p.add_argument("--reviewer", choices=["claude", "codex"], required=True)
    p.add_argument("--status", choices=["pending", "in_progress", "blocked"], default="in_progress")
    p.add_argument("--head-commit", default=None)
    p.add_argument("--notes", default="")
    p.set_defaults(func=cmd_new_task)

    p = sub.add_parser("send")
    p.add_argument("--task", required=True)
    p.add_argument("--from", dest="sender", choices=["human", "claude", "codex"], required=True)
    p.add_argument("--to", choices=["human", "claude", "codex"], required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--body-file")
    p.add_argument("--in-reply-to", default=None)
    p.add_argument("--status", default="open", choices=["open", "closed", "superseded"])
    p.add_argument("--task-status", choices=["pending", "in_progress", "blocked"])
    p.set_defaults(func=cmd_send)

    p = sub.add_parser("inbox")
    p.add_argument("agent", choices=["claude", "codex"])
    p.set_defaults(func=cmd_inbox)

    p = sub.add_parser("read")
    p.add_argument("task")
    p.set_defaults(func=cmd_read)

    p = sub.add_parser("complete")
    p.add_argument("task")
    p.add_argument("--from", dest="sender", choices=["human", "claude", "codex"], default="human")
    p.set_defaults(func=cmd_complete)

    p = sub.add_parser("archive")
    p.add_argument("task")
    p.set_defaults(func=cmd_archive)

    p = sub.add_parser("summarize")
    p.add_argument("task")
    p.set_defaults(func=cmd_summarize)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
