# Agent Bridge v2 Roadmap

## Summary

Agent Bridge v2 should not be a rewrite.

The core idea is still right:

- files remain the source of truth
- coordination correctness matters more than model-call orchestration
- the bridge should stay portable, repo-local, and inspectable

What needs to improve is the correctness guarantees around the existing file-based CLI.

The biggest pain in real use is not storage, and not the interface. It is correctness:

- schemas exist, but writes are not actually validated
- task state is too coarse for real review loops
- agent identities are hard-coded
- stuck locks, orphan tasks, and board drift are hard to diagnose quickly

The CLI (`bridge.py`) stays as the only interface in v2. Adding an MCP layer, daemon, or server would break the "copy `.agent-bridge/` folder, done" property that makes this tool portable, and the concrete pains above can all be solved without changing the interface model.

## Principles

- Keep files as the only source of truth.
- Keep the CLI as the only interface. No MCP, no daemon, no server in v2.
- Preserve the "copy folder, done" property — `.agent-bridge/` stays a self-contained drop-in.
- Improve correctness before adding convenience features.
- Timebox v2 to roughly one focused week.
- If a feature adds a second source of truth, skip it.

## Non-Goals

These are explicitly out of scope for v2:

- MCP server, daemon, or any long-running process alongside `.agent-bridge/`
- SQLite or Postgres indexing
- web dashboard
- generalized multi-agent scheduler
- automatic board generation
- naive file-overlap enforcement based only on filename matching

## V2 Core

These are the highest-value items and should be treated as the v2 cut line.

| Priority | Item | Pain Solved | Effort | Why Now |
|---|---|---|---|---|
| P0 | Write-time schema validation | Prevents invalid task/message JSON from becoming durable state | 0.5 day | The repo already claims schema-driven coordination; v2 should make that true |
| P0 | Explicit task phase state machine | Removes ambiguity between implementing, awaiting review, changes requested, blocked, and done | 1 day | Review loops are the core workflow and deserve first-class state |
| P0 | Agent registry | Removes hard-coded `human` / `claude` / `codex` assumptions | 0.5 day | Small change with high reuse across future projects |
| P0 | `bridge doctor` v1 | Detects stale locks and orphan tasks early | 0.5 day | These are the cheapest high-frequency failures to catch first |
| P0 | CLI output and error polish | Cleaner `--json` output, non-zero exit codes on validation failure, clearer error messages | 0.5 day | Keeps the CLI comfortable enough that no interface layer is needed |

## V2.1

These are the next items after the core is in use in a real project.

| Priority | Item | Pain Solved | Effort | Why Later |
|---|---|---|---|---|
| P1 | `TASK_BOARD` validation | Detects board/bridge drift without making the board machine-owned | 1 day | Useful, but secondary to the core correctness items |
| P1 | Claim / handoff / reassign commands | Makes task ownership transitions explicit instead of ad hoc | 1 day | Important once more than one active task is common |
| P1 | Notification polish | Better hooks when inboxes change or review is requested | 0.5-1 day | Helpful, but not correctness-critical |
| P1 | Write-intent metadata | Distinguishes “reviewing same file” from “two writers on same scope” | 1-2 days | Better than naive overlap checks, but needs more design |
| P1 | `bridge doctor` v1.1 | Adds phase-transition and missing-reference checks after the phase model is locked | 0.5-1 day | These checks depend on the state machine being defined clearly |

## Recommended Technical Shape

### 1. Keep the storage model

Do not replace the file-backed task and thread layout.

Current JSON files are easy to inspect, easy to diff, and cheap to copy into another repository. That is a feature, not a limitation.

### 2. Keep `bridge.py` as the single interface

Do not split logic out of `bridge.py` in v2.

The CLI is the interface contract both agents already use. Extracting a separate core module is only worthwhile if a second caller (MCP, daemon, library) is being added. V2 is not adding any of those.

What v2 does invest in on the CLI itself:

- structured `--json` output so agents can parse returns cleanly
- non-zero exit codes and structured error bodies on validation failure
- clearer, more specific error messages
- idempotent writes where cheap (a retried `send` should not create a duplicate message)

These are small, local changes that make the CLI comfortable enough that an additional interface layer has no reason to exist.

### 3. Introduce explicit task phases

Keep the board-level status coarse, but make the bridge track a richer live phase.

Recommended bridge phases:

- `claimed`
- `implementing`
- `awaiting_review`
- `changes_requested`
- `blocked`
- `done`

Recommended allowed transitions:

| From | Allowed To | Notes |
|---|---|---|
| `claimed` | `implementing`, `blocked` | Task has been accepted but active work has not started yet |
| `implementing` | `awaiting_review`, `blocked`, `done` | Direct `done` is only for work that does not require a peer review round |
| `awaiting_review` | `changes_requested`, `implementing`, `blocked`, `done` | A stale review notice routes the task back to `implementing`; it is not its own long-lived phase |
| `changes_requested` | `implementing`, `blocked` | Assignee resumes work or explicitly blocks |
| `blocked` | `claimed`, `implementing`, `awaiting_review` | `blocked` is an interrupt state; resume to the most appropriate live phase |
| `done` | none | Reopened work should be modeled as a new task or an explicit follow-up |

`bridge doctor` should enforce this table rather than infer transitions from message history with hidden assumptions.

Board status can stay:

- `Todo`
- `Active`
- `Blocked`
- `Done`

### 4. Add an agent registry

Move the actor list out of hard-coded enums and into config.

Minimal version:

- `agents.json` or similar config file
- display name
- role hints
- inbox path
- whether the actor is a human or an agent

That keeps the bridge reusable without changing code for every new project.

### 4.5. Define validation behavior and migration posture

Validation should fail closed on write:

- CLI returns non-zero on invalid task or message payloads
- error output is structured (JSON on `--json`, human-readable otherwise)
- invalid data is not written to the bridge files

For existing v1 bridge data:

- v2 should keep read compatibility for existing tasks and threads
- if new required fields are introduced, provide a one-shot migration path such as `bridge doctor --migrate-v1`
- migration should backfill sensible defaults rather than forcing humans to hand-edit old task files

### 5. Validate the board contract, do not auto-generate it yet

For projects that use `docs/TASK_BOARD.md`:

- each `Active` task must reference exactly one bridge task
- bridge tasks should optionally record the board task ID
- validation should check for missing or conflicting links

Do not make the board generated in v2. Human-edited planning is still the right default.

## Definition Of Done For v2

V2 is done when all of the following are true:

- two agents can coordinate through Agent Bridge via the CLI without relying on a human to manually relay structured state
- invalid task and message payloads are rejected on write
- active tasks expose an explicit live phase with enforced transitions
- adding a new agent does not require code edits to hard-coded enums
- there is a cheap diagnostic path for stale locks and orphan tasks
- `.agent-bridge/` remains a single folder that can be copied into another repo without extra setup
- the system still uses files as its only source of truth

## Cut Line

If time runs short, ship only this:

1. schema validation on write
2. explicit phase state with transition table
3. agent registry
4. `bridge doctor` v1 (stale locks + orphan tasks)
5. CLI output and error polish

That is the real v2.

Everything else can follow after the next project proves the need.
