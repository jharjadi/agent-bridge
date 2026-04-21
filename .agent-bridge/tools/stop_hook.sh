#!/usr/bin/env bash
# Claude stop-hook helper. Compares the current Claude inbox with the last
# observed snapshot and emits a JSON payload only when there are new messages
# from senders other than Claude.

set -uo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
root_dir="$(cd -- "${script_dir}/.." && pwd)"
state_file="${TMPDIR:-/tmp}/claude-bridge-stop-state.json"

inbox=$(python3 "${root_dir}/tools/bridge.py" inbox claude 2>/dev/null || echo "[]")
[ "${inbox}" = "[]" ] && exit 0

current=$(printf '%s' "${inbox}" | jq -c '[.[] | {task_id, latest_message_id, from, latest_type, summary}]')
prev=$(cat "${state_file}" 2>/dev/null || echo "[]")

new=$(jq -n --argjson cur "${current}" --argjson prev "${prev}" '
  [
    $cur[]
    | select(.from != "claude")
    | . as $c
    | if (($prev | map(select(.task_id == $c.task_id)) | first // {}).latest_message_id) == $c.latest_message_id
      then empty
      else $c
      end
  ]
')

printf '%s\n' "${current}" > "${state_file}"

count=$(printf '%s' "${new}" | jq 'length')
[ "${count}" -eq 0 ] && exit 0

summary=$(printf '%s' "${new}" | jq -r 'map("- \(.task_id) [\(.from)/\(.latest_type)]: \(.summary)") | join("\n")')
jq -n --arg msg "[Bridge] Inbox updated (${count} new from non-claude):\n${summary}" '{systemMessage: $msg}'
