# Agent Bridge

`agent-bridge/` is a portable, file-based coordination layer for a two-agent workflow where Codex usually implements and Claude usually reviews.

It is designed to be copied into another repository as a self-contained folder. The live workflow is append-only, task-based, and Git-friendly:

- one task record per task
- one thread folder per task
- one file per message
- one inbox pointer per agent
- review requests bound to exact commits
- runtime state ignored by Git by default

## What is included

- `tools/bridge.py`: the CLI for creating tasks, sending messages, reading inboxes, completing tasks, archiving threads, and generating summaries
- `tools/stop_hook.sh`: optional helper for notifying Claude when new non-Claude inbox messages arrive
- `schemas/`: JSON schemas for tasks and messages
- `AGENTS.md`, `CODEX.md`, `CLAUDE.md`: ready-to-copy operating instructions
- scaffold directories for runtime data
- `examples/proforma-task/`: a non-live example task and thread for reference

## What is intentionally not included

This starter kit does not ship with any live project state:

- no real inbox messages
- no real task registry entries
- no real thread history
- no real `state/*.json`
- no real `registry/index.json`

Those files are created automatically when the bridge is used.

## Install into another repository

1. Copy the entire `agent-bridge/` folder into the root of the target repository.
2. Commit the folder as part of that repository.
3. Tell both agents to read:
   - `agent-bridge/AGENTS.md`
   - `agent-bridge/CODEX.md`
   - `agent-bridge/CLAUDE.md`
4. Start using the bridge with:

```bash
python3 agent-bridge/tools/bridge.py inbox codex
```

If your team prefers a hidden folder, you can rename `agent-bridge/` to `.agent-bridge/`. The Python tool detects its folder name automatically. Just update the instruction paths and command examples accordingly.

## Runtime layout

```text
agent-bridge/
  archive/
  examples/
    proforma-task/
  inbox/
    claude/
    codex/
  locks/
  registry/
    tasks/
  schemas/
  state/
  threads/
  tools/
    bridge.py
    stop_hook.sh
  AGENTS.md
  CLAUDE.md
  CODEX.md
  README.md
```

## Core workflow

### 1. Create a task

```bash
python3 agent-bridge/tools/bridge.py new-task \
  --title "Implement login retry backoff" \
  --assigned-to codex \
  --reviewer claude
```

This creates:

- `registry/tasks/TASK-...json`
- `threads/TASK-.../0001-task-created.json`
- `inbox/codex/TASK-...json`

### 2. Send progress or questions

Prepare a JSON body file first:

```json
{
  "notes": [
    "Retry policy added",
    "Tests still pending"
  ]
}
```

Then send it:

```bash
python3 agent-bridge/tools/bridge.py send \
  --task TASK-20260421-001 \
  --from codex \
  --to claude \
  --type status_update \
  --summary "Implementation underway" \
  --body-file /tmp/body.json
```

### 3. Request review

```bash
python3 agent-bridge/tools/bridge.py send \
  --task TASK-20260421-001 \
  --from codex \
  --to claude \
  --type review_request \
  --summary "Ready for review" \
  --body-file /tmp/review-request.json
```

Review requests should include:

- `goal`
- `files_changed`
- `review_focus`
- `base_commit`
- `head_commit`

### 4. Read inbox and thread

```bash
python3 agent-bridge/tools/bridge.py inbox claude
python3 agent-bridge/tools/bridge.py read TASK-20260421-001
python3 agent-bridge/tools/bridge.py summarize TASK-20260421-001
```

### 5. Complete and archive

```bash
python3 agent-bridge/tools/bridge.py complete TASK-20260421-001 --from codex
python3 agent-bridge/tools/bridge.py archive TASK-20260421-001
```

## Runtime files and Git

The packaged `.gitignore` keeps live runtime state out of version control while preserving the empty scaffold folders and example files.

That means teams can:

- commit the bridge tooling and docs once
- use it every day without polluting Git with transient inbox or state files
- keep example material available for onboarding

## Example files

`examples/proforma-task/` shows a complete sample task record plus a small review cycle without placing those files into the live runtime folders.

Use it to:

- understand the expected JSON shapes
- onboard teammates
- copy body structures into real review requests or review responses

## Notes

- `bridge.py` uses atomic file replacement when writing JSON so readers do not see partial files.
- Message ids are allocated automatically. Do not hand-edit them.
- The bridge itself is intentionally simple. Teams can layer their own backlog docs, hooks, or automation on top.
