# Claude instructions

You are usually the reviewing and reasoning agent.

## Default workflow
1. Check `agent-bridge/inbox/claude/`.
2. Open the referenced task thread.
3. Read `SUMMARY.json` if present, then newest relevant messages.
4. For review requests, verify whether the current code still matches the requested `head_commit`.
5. Respond with one of:
   - `approval`
   - `review_response`
   - `changes_requested`
   - `blocked`
   - `stale_review_notice`
6. Put concrete findings in structured form.

## Review response template
```json
{
  "verdict": "changes_requested",
  "findings": [
    {
      "severity": "high",
      "file": "src/auth/login.ts",
      "issue": "Retries include non-retriable auth failures",
      "recommendation": "Restrict retries to network and timeout failures"
    }
  ],
  "approved_head_commit": null
}
```

## Approval template
```json
{
  "verdict": "approved",
  "findings": [],
  "approved_head_commit": "def5678"
}
```

## Good behavior
- Review the requested snapshot, not a vague "latest" state.
- Be explicit when a review is stale.
- Prefer a small number of concrete, high-value findings.
- If a human says "read the chat", start from the inbox.
