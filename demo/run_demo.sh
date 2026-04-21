#!/bin/bash

# 🎬 Agent Bridge Demo: Complete Collaboration Workflow
# This script demonstrates a full agent collaboration cycle

set -e  # Exit on any error

echo "🚀 Agent Bridge Demo: Live Agent Collaboration"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m' 
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper function for pretty output
demo_step() {
    echo -e "${BLUE}📋 $1${NC}"
    echo ""
}

demo_result() {
    echo -e "${GREEN}✅ $1${NC}"
    echo ""
}

demo_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
    echo ""
}

# Change to the project root
cd "$(dirname "$0")/.."

demo_step "Step 1: Setting up demo environment"

# Create a temporary demo file to work with
mkdir -p demo/src
cat > demo/src/calculator.py << 'EOF'
def add(a, b):
    return a + b

def multiply(a, b):
    # TODO: Implement multiplication
    pass
EOF

demo_result "Created demo source file: demo/src/calculator.py"

demo_step "Step 2: Creating a new collaboration task"

# Create task using bridge.py
TASK_OUTPUT=$(python3 .agent-bridge/tools/bridge.py new-task \
    --title "Implement multiplication function" \
    --assigned-to codex \
    --reviewer claude \
    --description "Add multiplication function to calculator module")

# Extract task ID from output
TASK_ID=$(echo "$TASK_OUTPUT" | grep -o "TASK-[A-Za-z0-9-]*" | head -1)

demo_result "Created task: $TASK_ID"
demo_info "Task assigned to: codex (implementation)"
demo_info "Reviewer assigned: claude (code review)"

demo_step "Step 3: Checking agent inboxes"

echo "📮 Codex inbox:"
python3 .agent-bridge/tools/bridge.py inbox codex
echo ""

echo "📮 Claude inbox:"  
python3 .agent-bridge/tools/bridge.py inbox claude
echo ""

demo_step "Step 4: Simulating implementation work (Codex)"

# Create implementation update message
cat > demo/implementation_update.json << EOF
{
    "notes": [
        "Implemented multiplication function",
        "Added input validation",
        "Function now handles edge cases"
    ],
    "files_changed": [
        "demo/src/calculator.py"
    ],
    "implementation_details": {
        "approach": "Simple multiplication with type checking",
        "edge_cases_handled": ["zero multiplication", "negative numbers"],
        "testing_status": "Ready for review"
    }
}
EOF

# Update the calculator file to show "implementation"
cat > demo/src/calculator.py << 'EOF'
def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers with input validation."""
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both arguments must be numbers")
    return a * b
EOF

# Send implementation update
python3 .agent-bridge/tools/bridge.py send \
    --task-id "$TASK_ID" \
    --message-type status_update \
    --body demo/implementation_update.json

demo_result "Codex completed implementation and sent update"

demo_step "Step 5: Requesting code review"

# Create review request
cat > demo/review_request.json << EOF
{
    "goal": "Review multiplication function implementation for correctness and best practices", 
    "files_changed": [
        "demo/src/calculator.py"
    ],
    "review_focus": [
        "Input validation logic",
        "Error handling approach", 
        "Code style and documentation",
        "Edge case coverage"
    ],
    "implementation_notes": "Added type checking and comprehensive docstring",
    "base_commit": "$(git rev-parse HEAD~1 2>/dev/null || echo 'initial')",
    "head_commit": "$(git rev-parse HEAD)"
}
EOF

python3 .agent-bridge/tools/bridge.py send \
    --task-id "$TASK_ID" \
    --message-type review_request \
    --body demo/review_request.json

demo_result "Codex requested code review from Claude"

demo_step "Step 6: Checking updated inboxes"

echo "📮 Claude inbox (new review request):"
python3 .agent-bridge/tools/bridge.py inbox claude
echo ""

demo_step "Step 7: Simulating code review (Claude)"

# Create review response  
cat > demo/review_response.json << EOF
{
    "verdict": "changes_requested",
    "findings": [
        {
            "severity": "medium",
            "file": "demo/src/calculator.py", 
            "line": 8,
            "issue": "Type checking could be more comprehensive",
            "recommendation": "Consider using numbers.Number for broader numeric type support"
        },
        {
            "severity": "low",
            "file": "demo/src/calculator.py",
            "issue": "Missing unit tests",
            "recommendation": "Add test cases for edge cases mentioned in implementation"
        }
    ],
    "positive_feedback": [
        "Good docstring documentation",
        "Appropriate error handling with TypeError",
        "Clean, readable implementation"
    ],
    "approved_head_commit": null,
    "next_steps": "Address type checking suggestion and add basic tests"
}
EOF

python3 .agent-bridge/tools/bridge.py send \
    --task-id "$TASK_ID" \
    --message-type review_response \
    --body demo/review_response.json

demo_result "Claude completed code review with change requests"

demo_step "Step 8: Simulating implementation improvements (Codex)"

# Update implementation based on feedback
cat > demo/src/calculator.py << 'EOF'
import numbers

def add(a, b):
    """Add two numbers."""
    return a + b

def multiply(a, b):
    """Multiply two numbers with comprehensive input validation."""
    if not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
        raise TypeError("Both arguments must be numbers")
    return a * b

# Basic test cases
if __name__ == "__main__":
    # Test normal cases
    assert multiply(3, 4) == 12
    assert multiply(-2, 5) == -10
    assert multiply(0, 100) == 0
    
    # Test edge cases  
    try:
        multiply("3", 4)
        assert False, "Should raise TypeError"
    except TypeError:
        pass
    
    print("All tests passed!")
EOF

# Send changes applied message
cat > demo/changes_applied.json << EOF
{
    "notes": [
        "Updated type checking to use numbers.Number",
        "Added comprehensive test cases",
        "All review feedback addressed"
    ],
    "files_changed": [
        "demo/src/calculator.py"
    ],
    "changes_made": {
        "type_checking": "Switched to numbers.Number for broader compatibility",
        "testing": "Added inline test cases with edge case coverage",
        "validation": "Maintained proper error handling"
    },
    "ready_for_final_review": true
}
EOF

python3 .agent-bridge/tools/bridge.py send \
    --task-id "$TASK_ID" \
    --message-type changes_applied \
    --body demo/changes_applied.json

demo_result "Codex addressed all review feedback"

demo_step "Step 9: Final review and approval (Claude)"

# Create approval response
cat > demo/approval.json << EOF
{
    "verdict": "approved",
    "findings": [
        {
            "severity": "none",
            "issue": "All previous concerns addressed",
            "recommendation": "Code ready for production"
        }
    ],
    "approval_notes": [
        "Excellent use of numbers.Number for type checking",
        "Comprehensive test coverage including edge cases",
        "Clean, maintainable implementation",
        "Good error handling and documentation"
    ],
    "approved_head_commit": "$(git rev-parse HEAD)",
    "quality_score": "excellent"
}
EOF

python3 .agent-bridge/tools/bridge.py send \
    --task-id "$TASK_ID" \
    --message-type approval \
    --body demo/approval.json

demo_result "Claude approved the implementation"

demo_step "Step 10: Completing the task"

python3 .agent-bridge/tools/bridge.py complete --task-id "$TASK_ID"

demo_result "Task completed successfully!"

demo_step "Step 11: Viewing the collaboration history"

echo "📊 Task Summary:"
if [ -f ".agent-bridge/threads/$TASK_ID/SUMMARY.json" ]; then
    cat ".agent-bridge/threads/$TASK_ID/SUMMARY.json"
else
    echo "Task thread messages:"
    ls -la ".agent-bridge/threads/$TASK_ID/" | head -10
fi
echo ""

echo "📁 Generated Files:"
echo "  - Task registry: .agent-bridge/registry/tasks/$TASK_ID.json"
echo "  - Thread history: .agent-bridge/threads/$TASK_ID/"
echo "  - Implementation: demo/src/calculator.py"
echo ""

demo_step "Step 12: Running the final implementation"

echo "🧮 Testing the completed calculator:"
python3 demo/src/calculator.py

echo ""
demo_result "Demo completed successfully! 🎉"
echo ""
echo "🔍 What happened:"
echo "  1. Task created and assigned to agents"
echo "  2. Implementation agent (Codex) wrote the code"  
echo "  3. Review agent (Claude) provided structured feedback"
echo "  4. Implementation agent addressed all feedback"
echo "  5. Review agent approved the final version"
echo "  6. Task marked as completed"
echo ""
echo "🎯 Key Benefits Demonstrated:"
echo "  ✅ Structured agent communication"
echo "  ✅ Git-friendly, append-only workflow"
echo "  ✅ Commit-bound code reviews"  
echo "  ✅ Complete audit trail"
echo "  ✅ Resumable collaboration"
echo ""
echo "🚀 Ready to use Agent Bridge in your own projects!"

# Cleanup
rm -f demo/implementation_update.json
rm -f demo/review_request.json  
rm -f demo/review_response.json
rm -f demo/changes_applied.json
rm -f demo/approval.json