# 🎬 Agent Bridge Demo: Live Collaboration Showcase

This directory contains interactive demonstrations of Agent Bridge in action.

## 🚀 Quick Demo Script

Run this script to see a complete agent collaboration workflow:

```bash
./demo/run_demo.sh
```

This will:
1. Create a sample task
2. Show agent inbox management
3. Demonstrate review workflow
4. Display final collaboration results

## 📋 Demo Scenarios

### Scenario 1: Code Review Workflow
**File**: `demo_code_review.sh`

Simulates:
- Codex implementing a new feature
- Claude reviewing the implementation
- Codex addressing feedback
- Claude approving the final version

### Scenario 2: Documentation Collaboration  
**File**: `demo_documentation.sh`

Demonstrates:
- Task creation for documentation
- Collaborative writing process
- Review and refinement cycle
- Final approval workflow

### Scenario 3: Multi-Task Coordination
**File**: `demo_multi_task.sh`

Shows:
- Multiple parallel tasks
- Agent workload balancing
- Cross-task dependencies
- Completion coordination

## 🎯 Interactive Demo

For a hands-on experience:

```bash
# 1. Create a real task
python3 ../.agent-bridge/tools/bridge.py new-task \
  --title "Demo: Add welcome message" \
  --assigned-to codex \
  --reviewer claude

# 2. Check the created files
ls ../.agent-bridge/registry/tasks/
ls ../.agent-bridge/threads/

# 3. View agent inboxes
python3 ../.agent-bridge/tools/bridge.py inbox codex
python3 ../.agent-bridge/tools/bridge.py inbox claude

# 4. Send a progress message (create demo_message.json first)
cat > demo_message.json << EOF
{
  "notes": ["Implemented welcome message function"],
  "files_changed": ["src/welcome.py"],
  "commits": ["abc123"]
}
EOF

python3 ../.agent-bridge/tools/bridge.py send \
  --task-id [TASK-ID-FROM-STEP-1] \
  --message-type status_update \
  --body demo_message.json
```

## 📊 Understanding the Demo Output

Each demo generates:
- **Task Files**: In `../.agent-bridge/registry/tasks/`
- **Thread History**: In `../.agent-bridge/threads/[TASK-ID]/`
- **Inbox Messages**: In `../.agent-bridge/inbox/[agent]/`
- **Summary Reports**: Generated automatically

## 🔧 Customizing Demos

Edit the demo scripts to:
- Change agent names
- Modify task scenarios
- Add custom message types
- Simulate different workflows

## 🎥 Demo Video Script

Follow this script to record a compelling demo:

### Opening (30 seconds)
"Welcome to Agent Bridge - let me show you how AI agents collaborate using structured, Git-friendly workflows..."

### Task Creation (1 minute)
"First, we create a task and assign it to our implementation agent..."
```bash
python3 .agent-bridge/tools/bridge.py new-task --title "Add user authentication" --assigned-to codex --reviewer claude
```

### Agent Workflow (2 minutes)  
"The agent checks its inbox, works on the task, and requests review..."
```bash
python3 .agent-bridge/tools/bridge.py inbox codex
# Show implementation work
python3 .agent-bridge/tools/bridge.py send --message-type review_request
```

### Review Process (1 minute)
"The review agent examines the code and provides structured feedback..."
```bash
python3 .agent-bridge/tools/bridge.py inbox claude
# Show review process
python3 .agent-bridge/tools/bridge.py send --message-type review_response
```

### Completion (30 seconds)
"After addressing feedback, the task is approved and completed - all tracked in Git!"

## 🚀 Live Demo Tips

1. **Prepare Sample Files**: Have realistic code files ready
2. **Use Real Commits**: Show actual Git integration
3. **Highlight Structure**: Emphasize the JSON message format
4. **Show Scalability**: Demonstrate multiple concurrent tasks
5. **Emphasize Benefits**: Focus on auditability and resumability

---

**Ready to showcase the future of AI collaboration?** 🤖✨