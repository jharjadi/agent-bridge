# Codex instructions

You are usually the implementing agent.

## Default workflow
1. Read the assigned task.
2. Implement the requested changes.
3. Post status updates only when useful.
4. When ready, send a `review_request` to Claude through `agent-bridge/tools/bridge.py`.
5. Include all files changed and the exact `head_commit`.
6. If Claude requests changes, implement them and send `changes_applied` or a new `review_request`.
7. When Claude approves, mark the task complete.

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
- Keep Claude’s review targeted.
- Mention any known risks.
- Supersede older review requests by sending a newer one.
- If the human says "send to Claude", do that through the bridge, not plain text chat.
