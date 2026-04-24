# Task Board

## Purpose

`docs/TASK_BOARD.md` is the human planning board for this repository.

It exists to make backlog, ownership, scope, and dependencies readable to humans without turning the board into a live chat log.

`.agent-bridge/` remains the source of truth for active agent coordination, review state, and commit-bound execution history.

## Source Of Truth Contract

### `docs/TASK_BOARD.md` owns

- task ID, title, track, and priority
- lead owner for the task
- coarse status: `Todo`, `Active`, `Blocked`, `Done`
- file scope
- dependencies
- spec summary and done criteria
- human notes that matter for planning

### `.agent-bridge/` owns

- current assignee and reviewer for the active round
- message history
- review requests and review responses
- stale review notices
- current `head_commit`
- live execution phase such as implementation, awaiting review, or changes requested
- completion events and thread archive history

### Rules

- A board task moves to `Active` only when exactly one bridge task exists for it.
- Active work must include a `Bridge Task` reference in the board row and task details.
- Do not create a second hand-maintained “live bridge tasks” table. Put the bridge task ID on the main task row instead.
- The board should not track fine-grained agent workflow states such as `awaiting_review` or `changes_requested`. Those belong in `.agent-bridge/`.
- If the board and bridge disagree about live execution state, trust the bridge and then update the board.

## Operating Rules

- Pick up a task:
  - set `Status` to `Active`
  - set `Lead`
  - confirm the file scope
  - create the corresponding bridge task
- Finish a task:
  - set `Status` to `Done`
  - note the commit or PR in `Notes`
  - complete the bridge task if one exists
- Block a task:
  - set `Status` to `Blocked`
  - record the blocker in `Depends On` or `Notes`
  - send a bridge update if the task is already active
- Ownership boundary:
  - file scope is the coordination boundary
  - two active tasks must not have overlapping file scopes unless a human explicitly approves it
- Update discipline:
  - update this board in the same commit that materially changes task status or scope

## Status Key

| Status | Meaning |
|---|---|
| `Todo` | Ready to start, not yet claimed in the bridge |
| `Active` | Claimed and tracked by exactly one live bridge task |
| `Blocked` | Cannot progress because of a dependency, decision, or missing input |
| `Done` | Completed and closed; bridge task completed if one existed |

## Overview Table

| ID | Track | Title | Lead | Status | Priority | File Scope | Depends On | Bridge Task | Notes |
|---|---|---|---|---|---|---|---|---|---|
| T-EXAMPLE-01 | Example | Replace this sample row | Unassigned | `Todo` | P2 | `path/to/area/` | — | — | Delete or replace |

## Task Template

Copy this section for each task that needs more than a one-line row entry.

---

### T-EXAMPLE-01 — Replace this sample task

- Track: Example
- Lead: Unassigned
- Status: `Todo`
- Priority: P2
- File Scope: `path/to/area/`
- Depends On: nothing
- Bridge Task: none
- Spec:
  - describe the task in concrete engineering terms
  - prefer exact scope over broad intent
  - mention any design or correctness constraints that matter
- Done When:
  - give a checkable completion condition
  - include tests, docs, or verification expectations if they matter
- Notes:
  - use for planning notes, PR references, or human decisions

## Example Task

This is the intended level of specificity for a real task entry.

### T-INF-01 — AWS IaC (VPC/ECS/RDS/ALB/ACM/IAM)

- Track: Infra
- Lead: Codex
- Status: `Done`
- Priority: P1
- File Scope: `infra/`, `.github/workflows/`
- Depends On: nothing
- Bridge Task: `TASK-20260419-003`
- Spec:
  - IaC for all three environments: `dev`, `staging`, and `prod`
  - cover VPC, subnets, security groups, ALB, ECS cluster and service definitions, RDS, ECR repos, IAM task roles, Secrets Manager, SSM parameters, CloudWatch logs, and Route 53
  - tool confirmed for first pass: Terraform
- Done When:
  - `dev` provisions successfully
  - all services are healthy
  - corpus bootstrap works
- Notes:
  - use this level of precision for scope and completion criteria

## Recommended Conventions

- Use stable IDs like `T-AUTH-01` or `T-PERF-03`.
- Use `Lead` to mean the current human or agent primarily responsible for moving the task forward.
- Keep `Status` coarse on the board. Use the bridge thread for detailed workflow state.
- Keep completed sections concise. Archive detail in commits, PRs, and bridge history.
- Prefer one task per independently reviewable scope.

## What Not To Put Here

- long back-and-forth review discussion
- per-message agent updates
- stale copies of bridge thread summaries
- multiple competing task states across separate tables
- ambiguous file scopes like `web/` when the actual scope is much narrower

## Future Automation

This board is intentionally human-edited in V1.

If drift becomes a recurring problem, add tooling later to:

- validate that every `Active` task has a bridge task
- verify that active file scopes do not overlap
- cross-check board status against bridge status
- generate summary views for active bridge tasks
