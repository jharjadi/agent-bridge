# Contributing to Agent Bridge

Thanks for taking a look at the project.

This repository contains two related things:

- the packaged `.agent-bridge/` folder that can be copied into another repository
- docs and demos that explain how the workflow is meant to operate

Good contributions include fixes to the CLI, schema changes, documentation improvements, and better examples.

## Before You Start

Read these first:

- [README.md](README.md)
- [.agent-bridge/README.md](.agent-bridge/README.md)
- [.agent-bridge/examples/proforma-task/](.agent-bridge/examples/proforma-task/)

If your change affects agent instructions, also review:

- [.agent-bridge/AGENTS.md](.agent-bridge/AGENTS.md)
- [.agent-bridge/CODEX.md](.agent-bridge/CODEX.md)
- [.agent-bridge/CLAUDE.md](.agent-bridge/CLAUDE.md)

## Typical Contribution Flow

1. Create a branch for a focused change.
2. Make the smallest change that solves the problem clearly.
3. Update docs or examples if the CLI, schema, or workflow changed.
4. Run the relevant verification commands.
5. Open a pull request with a short explanation of what changed and how you checked it.

Direct pull requests are fine. If you want to use Agent Bridge itself while working on the repo, that is also fine, but it is not required for every contribution.

The bridge assigns roles per task. `assigned-to` and `reviewer` describe the current task, not fixed capabilities of `codex` or `claude`.

## Working With the Bridge

If you are testing or demonstrating the workflow itself, the main commands are:

Create a task:

```bash
python3 .agent-bridge/tools/bridge.py new-task \
  --title "Example contribution" \
  --assigned-to claude \
  --reviewer codex
```

Check an inbox:

```bash
python3 .agent-bridge/tools/bridge.py inbox codex
python3 .agent-bridge/tools/bridge.py inbox claude
```

Send a message:

```bash
python3 .agent-bridge/tools/bridge.py send \
  --task TASK-20260421-001 \
  --from claude \
  --to codex \
  --type status_update \
  --summary "Implementation underway" \
  --body-file /tmp/body.json
```

Read or summarize a thread:

```bash
python3 .agent-bridge/tools/bridge.py read TASK-20260421-001
python3 .agent-bridge/tools/bridge.py summarize TASK-20260421-001
```

Complete and archive a task:

```bash
python3 .agent-bridge/tools/bridge.py complete TASK-20260421-001 --from codex
python3 .agent-bridge/tools/bridge.py archive TASK-20260421-001
```

## What to Verify

Choose checks that fit the change you made. For most documentation or small CLI changes, these are a good baseline:

```bash
python3 .agent-bridge/tools/bridge.py --help
python3 .agent-bridge/tools/bridge.py new-task --help
python3 .agent-bridge/tools/bridge.py send --help
python3 .agent-bridge/tools/bridge.py inbox --help
python3 .agent-bridge/tools/bridge.py read --help
python3 .agent-bridge/tools/bridge.py complete --help
python3 .agent-bridge/tools/bridge.py archive --help
python3 .agent-bridge/tools/bridge.py summarize --help
```

If you changed workflow behavior or demo material, also run:

```bash
./demo/run_demo.sh
```

If you changed schemas or message shapes, make sure the docs and examples still match.

## Contribution Guidelines

- Keep changes focused. This repository is small, and narrow changes are easier to review.
- Prefer clear, literal wording over marketing language in docs.
- Keep examples aligned with the actual CLI.
- Preserve the current scope unless you are intentionally expanding it.
- Avoid committing live runtime state from `.agent-bridge/inbox/`, `.agent-bridge/threads/`, `.agent-bridge/registry/tasks/`, or `.agent-bridge/state/`.

## Pull Request Notes

When opening a pull request, it helps to include:

- the problem you were addressing
- the main files you changed
- any command output or manual checks you used to verify the change
- any follow-up work that is still out of scope
