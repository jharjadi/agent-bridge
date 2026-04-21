# Proforma Task Example

This folder contains a non-live example of a single task moving through a small Codex to Claude review cycle.

It is intentionally kept outside the live runtime folders so teams can copy `agent-bridge/` into a repository without inheriting fake inbox items or task state.

Included files:

- `task.json`: example task registry entry
- `thread/0001-task-created.json`: initial task creation message
- `thread/0002-review-request.json`: example Codex review request
- `thread/0003-review-response.json`: example Claude review response
- `thread/SUMMARY.json`: example generated summary

Use this folder as:

- a shape reference for task and message JSON
- onboarding material for new users
- a template source when drafting real body files
