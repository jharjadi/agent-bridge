# Agent Bridge

Agent Bridge is a portable, file-based coordination layer for two-agent workflows.

It is designed for workflows where task roles are explicit, but not tied to a specific agent identity. Either agent can implement or review on a given task. The bridge keeps that workflow explicit by storing tasks, messages, and review requests as files inside the repository.

This repository includes:

- `.agent-bridge/`: the packaged bridge folder you can copy into another repository
- `demo/`: small scripts that demonstrate the workflow end to end
- top-level docs and draft material used to explain the project

## What It Does

Agent Bridge is built around a few constraints:

- file-based runtime state instead of a database or service
- append-only task threads and inbox pointers
- review requests bound to exact commits
- JSON schemas for task and message structure
- a layout that can be copied into another repository as-is

The current starter kit is intentionally narrow in scope. It is designed for a two-agent workflow, not a general orchestration framework.

## Why Use It

Most of the value comes from making agent handoffs more explicit:

- tasks have durable records
- review requests can point to a specific code state
- inboxes make pending work visible
- runtime files can stay out of Git while the tooling stays in Git

If your team wants a lightweight coordination layer that can live inside an existing repository, that is the use case this project is aimed at.

## Quick Start

### Run the demo

```bash
./demo/run_demo.sh
```

The demo walks through task creation, inbox handling, review requests, and completion.

### Install into another repository

1. Copy `.agent-bridge/` into the root of the target repository.
2. Commit it as part of that repository.
3. Tell both agents to read:
   - `.agent-bridge/AGENTS.md`
   - `.agent-bridge/CODEX.md`
   - `.agent-bridge/CLAUDE.md`

If you prefer a visible folder name, you can rename `.agent-bridge/` to `agent-bridge/`. The CLI detects the folder name automatically, but you should update your instruction paths and examples to match.

## Basic Workflow

Create a task:

```bash
python3 .agent-bridge/tools/bridge.py new-task \
  --title "Implement user authentication" \
  --assigned-to claude \
  --reviewer codex
```

Check an inbox:

```bash
python3 .agent-bridge/tools/bridge.py inbox claude
```

Send a review request:

```bash
python3 .agent-bridge/tools/bridge.py send \
  --task TASK-20260421-001 \
  --from claude \
  --to codex \
  --type review_request \
  --summary "Ready for review" \
  --body-file /tmp/review-request.json
```

Read a task thread:

```bash
python3 .agent-bridge/tools/bridge.py read TASK-20260421-001
```

Complete and archive it:

```bash
python3 .agent-bridge/tools/bridge.py complete TASK-20260421-001 --from codex
python3 .agent-bridge/tools/bridge.py archive TASK-20260421-001
```

## Repository Layout

The packaged bridge lives in `.agent-bridge/` and includes:

- `tools/bridge.py`: the CLI
- `schemas/`: JSON schemas for tasks and messages
- `AGENTS.md`, `CODEX.md`, `CLAUDE.md`: instructions for participating agents
- scaffold directories for runtime state
- `examples/proforma-task/`: a reference task and thread

For a more detailed walkthrough of the packaged folder, see [.agent-bridge/README.md](.agent-bridge/README.md).

## Current Scope

This repository is intentionally modest in scope:

- the bridge is aimed at two-agent workflows
- runtime state is file-based
- there is no external service, dashboard, or dependency stack
- teams can layer their own automation on top if they need more

That makes it easier to copy, inspect, and adapt, but it also means it is not trying to solve every orchestration problem.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contributor workflow and verification guidance.

## License

MIT. See [LICENSE](LICENSE).
