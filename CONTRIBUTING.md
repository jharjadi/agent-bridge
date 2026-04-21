# Contributing to Agent Bridge 🤖

Thank you for your interest in contributing to Agent Bridge! This project demonstrates and facilitates AI agent collaboration, and we welcome both human and agent contributions.

## 🚀 How This Project Works

**Agent Bridge uses itself for development!** This means:

- Implementation work is typically done by AI agents (like Codex)
- Code reviews are typically done by AI agents (like Claude)  
- Humans provide oversight, guidance, and final approval
- All collaboration happens through the `.agent-bridge/` system

## 📋 Before Contributing

1. **Understand the Agent Bridge System**
   - Read the main [README.md](README.md)
   - Review [.agent-bridge/README.md](.agent-bridge/README.md) for technical details
   - Check out the [example workflow](.agent-bridge/examples/proforma-task/)

2. **Check Active Work**
   ```bash
   # See what's currently being worked on
   python3 .agent-bridge/tools/bridge.py list-tasks
   
   # Check agent inboxes
   python3 .agent-bridge/tools/bridge.py inbox claude
   python3 .agent-bridge/tools/bridge.py inbox codex
   ```

## 🤝 Contribution Workflows

### 🤖 AI Agent Contributors

If you're an AI agent wanting to contribute:

1. **Read the Agent Instructions**
   - [.agent-bridge/AGENTS.md](.agent-bridge/AGENTS.md) - General instructions
   - [.agent-bridge/CLAUDE.md](.agent-bridge/CLAUDE.md) - Claude-specific instructions
   - [.agent-bridge/CODEX.md](.agent-bridge/CODEX.md) - Codex-specific instructions

2. **Follow the Bridge Workflow**
   ```bash
   # Check your inbox first
   python3 .agent-bridge/tools/bridge.py inbox [your-agent-name]
   
   # Create or work on tasks using the bridge system
   python3 .agent-bridge/tools/bridge.py new-task --title "Your contribution"
   ```

3. **Maintain Quality Standards**
   - All messages must follow JSON schemas in `.agent-bridge/schemas/`
   - Include commit references for code reviews
   - Write clear, structured summaries
   - Respond to review feedback promptly

### 👥 Human Contributors

If you're a human contributor:

1. **Direct Contributions**
   - Fork the repository
   - Create a feature branch
   - Make your changes
   - Submit a pull request

2. **Coordinating Agent Work**
   ```bash
   # Create tasks for agents to work on
   python3 .agent-bridge/tools/bridge.py new-task \
     --title "Feature: Add new capability" \
     --assigned-to codex \
     --reviewer claude
   
   # Monitor and guide agent collaboration
   python3 .agent-bridge/tools/bridge.py inbox [agent]
   ```

3. **Improving the Bridge System**
   - Enhancements to `bridge.py` tool
   - New JSON schemas
   - Documentation improvements
   - Example workflows

## 🎯 Contribution Areas

### High Priority
- **Bridge Tool Enhancements**: New features for `bridge.py`
- **Schema Improvements**: Better message validation
- **Documentation**: More examples and use cases
- **Integration Examples**: GitHub Actions, webhooks, etc.

### Medium Priority  
- **Multi-Agent Support**: Beyond two-agent workflows
- **Notification Systems**: Slack, Discord integrations
- **Web Dashboard**: Visual interface for monitoring
- **Performance**: Optimizations for large-scale usage

### Ideas Welcome
- **Plugin System**: Custom workflow extensions
- **Analytics**: Collaboration metrics and insights
- **Testing Framework**: Automated workflow testing
- **Templates**: Ready-made collaboration patterns

## 📝 Standards & Guidelines

### Code Quality
- Follow existing code style and patterns
- Add tests for new functionality  
- Update documentation for changes
- Ensure backwards compatibility

### Agent Collaboration Quality
- Use structured JSON messages
- Include proper commit references
- Write clear task descriptions
- Provide actionable review feedback

### Documentation
- Update README.md for significant changes
- Add examples for new features
- Keep agent instructions current
- Document breaking changes

## 🧪 Testing Your Contributions

### Manual Testing
```bash
# Test basic bridge functionality
python3 .agent-bridge/tools/bridge.py --help

# Test task creation
python3 .agent-bridge/tools/bridge.py new-task --title "Test task" --assigned-to test

# Validate JSON schemas
python3 -c "import json; json.load(open('.agent-bridge/schemas/task.schema.json'))"
```

### Integration Testing
- Test with actual AI agents if possible
- Verify Git integration works correctly
- Check file locking under concurrent access
- Validate schema compliance

## 🚀 Getting Started

1. **Fork and Clone**
   ```bash
   git clone https://github.com/[your-username]/agent-bridge.git
   cd agent-bridge
   ```

2. **Set Up Development Environment**
   ```bash
   # No dependencies needed! Pure Python 3
   python3 .agent-bridge/tools/bridge.py --help
   ```

3. **Make Your First Contribution**
   - Start with documentation improvements
   - Fix small bugs or add minor features
   - Propose new examples or use cases

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas  
- **Agent Inbox**: If you're an AI agent, check your inbox in `.agent-bridge/inbox/`

## 🌟 Recognition

Contributors will be recognized in:
- README.md acknowledgments
- Release notes for significant contributions
- Agent Bridge showcase examples

---

**Remember**: This project is about demonstrating the future of AI collaboration. Every contribution helps show how agents and humans can work together effectively! 🚀

*Contributing to Agent Bridge means contributing to the future of AI teamwork.* ✨