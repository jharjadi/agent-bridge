## 🚀 Agent Bridge Pull Request

### 📋 Change Description

**Clear description of changes made**

### 🤖 Agent Collaboration Impact  

**How do these changes affect agent workflows?**

- [ ] Improves agent coordination
- [ ] Enhances message passing
- [ ] Updates agent instructions
- [ ] Modifies bridge tool functionality
- [ ] Changes schema definitions
- [ ] Updates documentation
- [ ] No impact on agent workflows

### 🔄 Type of Change

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that causes existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🧪 Test additions/improvements
- [ ] 🔧 Code refactoring (no functional changes)
- [ ] 🎨 Style/formatting changes

### 🧪 Testing Performed

**How were these changes tested?**

- [ ] Ran demo workflow: `./demo/run_demo.sh`  
- [ ] Tested bridge CLI: `python3 .agent-bridge/tools/bridge.py --help`
- [ ] Validated JSON schemas
- [ ] Tested with real agents (Claude/Codex)
- [ ] Manual testing performed
- [ ] Unit tests added/updated
- [ ] Integration tests verified

**Test commands run:**
```bash
# Add commands you used to test
```

### 📁 Files Changed

**Key files modified:**

- Bridge tool: `.agent-bridge/tools/bridge.py`
- Schemas: `.agent-bridge/schemas/`
- Documentation: 
- Agent instructions:
- Examples:
- Other:

### 🎯 Agent Instructions Updated

**If agent behavior changes, were instructions updated?**

- [ ] Updated `.agent-bridge/AGENTS.md`
- [ ] Updated `.agent-bridge/CLAUDE.md`  
- [ ] Updated `.agent-bridge/CODEX.md`
- [ ] No agent instruction changes needed
- [ ] N/A - not agent-facing changes

### 🔄 Backwards Compatibility

- [ ] ✅ Fully backwards compatible
- [ ] ⚠️ May affect existing workflows (explain below)
- [ ] 💥 Breaking changes (document migration path below)

**Compatibility notes:**

### 📊 Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review of code completed
- [ ] Code is commented, particularly complex areas
- [ ] Documentation updated for changes
- [ ] No new warnings introduced
- [ ] Tests pass locally
- [ ] Agent collaboration workflow still functional

### 🎬 Demo Impact

**Does this change affect the demo?**

- [ ] Demo updated to reflect changes
- [ ] Demo still works with changes  
- [ ] Demo needs updating (describe below)
- [ ] No demo impact

### 🔗 Related Issues

**Link related issues:**

Fixes #
Related to #

### 🤖 Agent Review Requests

**If using Agent Bridge for this PR:**

**Task ID:** TASK-_______________

**Agent coordination notes:**
- Implementation agent: 
- Review agent:
- Commit for review: `[commit-hash]`

### 📝 Additional Notes

**Any additional context or notes for reviewers**

---

### 🚀 Ready for Review

By submitting this PR, I confirm that:

- [ ] This change maintains the integrity of agent collaboration workflows
- [ ] All agent-facing changes are properly documented  
- [ ] The bridge system remains Git-friendly and append-only
- [ ] Changes follow the established JSON schema patterns
- [ ] This contribution helps advance AI agent collaboration 🤖✨