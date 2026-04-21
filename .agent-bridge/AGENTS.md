# Shared operating instructions for Claude and Codex

You are participating in a file-based agent bridge inside this repository.

## Objective
Use `agent-bridge/` as the default coordination channel between agents unless the human explicitly says otherwise.

If your team renames the folder to `.agent-bridge/`, use that path instead. The tooling is location-aware.

## Required behavior
1. Treat `registry/tasks/*.json` as task summaries.
2. Treat `threads/<task-id>/` as the source of truth.
3. Read your inbox first: `agent-bridge/inbox/<your-agent>/`.
4. If your repo also has a human-readable backlog or work board, keep it for planning, but keep live agent coordination in `agent-bridge/`.
5. When sending a new message, always use `python3 agent-bridge/tools/bridge.py send ...` or the equivalent path for your chosen folder name.
6. Do not hand-edit message ids.
7. Do not overwrite old messages.
8. Keep summaries short and structured.
9. Use exact task ids in every action.
10. If you are reviewing code, bind the review to a specific `head_commit`.
11. If the code changed after the review request commit, respond with `stale_review_notice` or clearly state that the review is stale.

## Message quality rules
- Summaries must be one sentence.
- Bodies must be valid JSON objects.
- Review requests must include: goal, files_changed, review_focus, base_commit, head_commit.
- Review responses must include: verdict, findings, approved_head_commit.
- When commit references matter, distinguish commits made in the current change from older historical commits referenced for context.
- If blocked, explain exactly what is missing.

## When told to "read the chat"
1. Check your inbox.
2. Open the active task or tasks relevant to the human instruction.
3. Read `SUMMARY.json` if present.
4. Read the newest messages addressed to you.
5. Reply in-thread.

## When a task is done
- Send `task_completed` or `approval`.
- Update the task through `bridge.py complete` if you are the acting agent and the human has not objected.
- Use `bridge.py complete` to mark a task as completed. `send --task-status` is only for `pending`, `in_progress`, or `blocked`.

## Forbidden patterns
- Do not create a global shared chat file.
- Do not use ad hoc markdown logs as the live message bus.
- Do not paste huge unstructured transcripts.
- Do not review code without recording the target commit.
- Do not silently change task ownership.
