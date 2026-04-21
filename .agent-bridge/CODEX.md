# Codex instructions

You can act as either the implementing agent or the reviewing agent, depending on the task.

## Default workflow
1. Read the assigned task.
2. Determine whether the task currently assigns you implementation work, review work, or follow-up work.
3. If you are implementing, make the requested changes and post status updates only when useful.
4. If you are reviewing, review the requested snapshot and respond in-thread with structured findings.
5. When sending a `review_request`, address it to the reviewer assigned on the task through `agent-bridge/tools/bridge.py`.
6. Include all files changed and the exact `head_commit` when asking for review.
7. If the reviewer requests changes, implement them and send `changes_applied` or a new `review_request`.
8. When the task is approved or complete, use the appropriate bridge message and completion step.

## Review request template
Use this body shape:

```json
{
  "goal": "Implement login retry backoff",
  "what_changed": [
    "Added retry policy",
    "Integrated retry policy into login flow",
    "Added tests"
  ],
  "files_changed": [
    "src/auth/retry.ts",
    "src/auth/login.ts",
    "tests/auth/retry.test.ts"
  ],
  "review_focus": [
    "correctness",
    "edge cases",
    "test coverage"
  ],
  "base_commit": "abc1234",
  "head_commit": "def5678"
}
```

## Good behavior
- Keep review requests targeted.
- Mention any known risks.
- Supersede older review requests by sending a newer one.
- If the human says to send work to another agent, do that through the bridge, not plain text chat.
