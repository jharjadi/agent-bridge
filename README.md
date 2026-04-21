# 🤖 Agent Bridge: File-Based AI Agent Collaboration System

> **A revolutionary coordination layer that enables structured collaboration between AI agents using Git-friendly, append-only workflows.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent-Friendly](https://img.shields.io/badge/Agent-Friendly-blue.svg)](.agent-bridge/)
[![Git-Native](https://img.shields.io/badge/Git-Native-green.svg)](.agent-bridge/.gitignore)

## 🚀 What is Agent Bridge?

Agent Bridge is a portable, file-based coordination system designed for **two-agent workflows** where different AI agents (like Codex and Claude) collaborate on tasks with clearly defined roles - typically one for implementation and another for review.

### ✨ Key Features

- **📁 File-Based**: Everything stored as JSON files - no databases, no servers
- **🔄 Git-Friendly**: Append-only design that works perfectly with version control
- **🎯 Task-Oriented**: One task record per task, one thread folder per task
- **🔒 Commit-Bound Reviews**: Reviews tied to exact Git commits for precision
- **📮 Inbox System**: Each agent has their own inbox for pending work
- **🏗️ Portable**: Drop into any repository as a self-contained folder

## 🏆 Why This Matters

Traditional AI agent collaboration often lacks structure and auditability. Agent Bridge solves this by providing:

1. **Structured Communication**: All messages follow JSON schemas
2. **Clear Accountability**: Every action is logged with timestamps and commits
3. **Resumable Workflows**: Agents can pick up where others left off
4. **Review Integrity**: Code reviews are bound to specific commits
5. **Human Oversight**: Transparent, file-based workflow humans can inspect

## 🎬 Live Demonstration

This repository **itself** demonstrates agent collaboration! The Agent Bridge system coordinates:

- **🔧 Implementation Agent** (typically Codex): Writes code, implements features
- **🔍 Review Agent** (typically Claude): Reviews code, provides feedback
- **👥 Human Oversight**: Monitors and guides the collaboration

## 🚀 Quick Start

### 1. Install into Your Repository

```bash
# Copy the entire .agent-bridge/ folder to your project root
cp -r .agent-bridge/ /path/to/your/project/

# Or rename to visible folder if you prefer
mv .agent-bridge/ agent-bridge/
```

### 2. Start Collaborating

```bash
# Create a new task
python3 .agent-bridge/tools/bridge.py new-task \
  --title "Implement user authentication" \
  --assigned-to codex \
  --reviewer claude

# Check your inbox
python3 .agent-bridge/tools/bridge.py inbox claude

# Send progress updates
python3 .agent-bridge/tools/bridge.py send \
  --task-id TASK-xxx \
  --message-type review_request \
  --body review_body.json
```

## 📋 Workflow Example

```
1. Human creates task → assigned to Implementation Agent
2. Implementation Agent works → requests review
3. Review Agent examines code → provides feedback
4. Implementation Agent applies changes → re-requests review  
5. Review Agent approves → task completed
```

Every step is logged, traceable, and resumable.

## 📁 Project Structure

```
.agent-bridge/
├── README.md              # Detailed technical documentation
├── AGENTS.md              # Shared operating instructions
├── CLAUDE.md              # Claude-specific instructions  
├── CODEX.md               # Codex-specific instructions
├── tools/
│   ├── bridge.py          # Main CLI tool
│   └── stop_hook.sh       # Notification helper
├── examples/
│   └── proforma-task/     # Example task & thread
├── schemas/               # JSON schemas for validation
├── inbox/                 # Agent inboxes (runtime)
├── registry/              # Task registry (runtime)
├── threads/               # Task conversations (runtime)
└── state/                 # System state (runtime)
```

## 🛠️ Technical Highlights

- **Zero Dependencies**: Pure Python 3, no external packages
- **Schema Validation**: All messages validated against JSON schemas
- **Atomic Operations**: File-based locking prevents race conditions
- **Git Integration**: Designed to work seamlessly with Git workflows
- **Cross-Platform**: Works on any system with Python 3

## 🎯 Use Cases

- **Code Review Workflows**: Automated code review with AI agents
- **Documentation Generation**: One agent writes, another reviews and refines
- **Testing Coordination**: Implementation and validation agents working together
- **Research Projects**: Structured collaboration between reasoning agents
- **Quality Assurance**: Systematic review processes for AI-generated content

## 🤝 Contributing to Agent Collaboration

This project itself uses Agent Bridge! To contribute:

1. Check active tasks: `python3 .agent-bridge/tools/bridge.py list-tasks`
2. Review agent inboxes: `python3 .agent-bridge/tools/bridge.py inbox [agent]`
3. Follow the collaboration patterns demonstrated in the examples

## 📚 Documentation

- **[Technical README](.agent-bridge/README.md)**: Complete implementation details
- **[Agent Instructions](.agent-bridge/AGENTS.md)**: How agents should behave
- **[Example Task](.agent-bridge/examples/proforma-task/)**: Sample workflow
- **[JSON Schemas](.agent-bridge/schemas/)**: Message format specifications

## 🔮 Future Possibilities

- Multi-agent workflows (beyond two agents)
- Integration with GitHub Actions
- Slack/Discord notifications
- Web dashboard for monitoring
- Plugin system for custom workflows

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Ready to revolutionize AI agent collaboration?** Drop Agent Bridge into your repository and watch structured, accountable AI teamwork in action! 🚀

*Built with ❤️ for the future of AI collaboration*