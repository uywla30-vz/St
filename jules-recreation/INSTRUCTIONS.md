# Jules Recreation: Development Roadmap & Instructions

This document outlines the phased development plan for enhancing the Jules AI agent recreation. Future agents or developers should follow this roadmap to improve the system's capabilities, performance, and user experience.

## Phase 1: Core Robustness & Context (Day 1-2)
*Goal: Move from basic tool use to sophisticated environment awareness.*

1. **Persistent Context Window**: Implement a mechanism to manage the model's context window. Instead of passing the entire history, summarize older observations or use a sliding window to maintain relevance without hitting token limits.
2. **Enhanced File Awareness**: Automatically scan the `workspace/` directory on startup and provide the agent with a "mental map" of existing files in the system prompt.
3. **Improved Error Handling**: Implement specialized retry logic for failed tool calls (e.g., if a command fails, the agent should analyze the `stderr` and propose a fix).

## Phase 2: Line-Level Editing (Day 3-5)
*Goal: Move beyond `write_file` (overwriting) to surgical code modifications.*

1. **Implement `edit_file` Tool**: Create a new tool that accepts:
   - `filepath`: The file to modify.
   - `search`: The exact string or regex to find.
   - `replace`: The new content to insert.
2. **Unified Diff Support**: Allow the agent to provide changes in `diff` format, similar to Git, which the backend will apply safely to the source files.
3. **Syntax Validation**: Before saving an `edit_file` action, run a lightweight syntax check (e.g., `python -m py_compile`) to ensure the edit didn't break the code.

## Phase 3: Advanced UI & Interactive terminal (Day 6-8)
*Goal: Elevate the web interface to a professional-grade IDE experience.*

1. **Monaco Editor Integration**: Replace the static code viewer with the Monaco Editor (the engine behind VS Code) for syntax highlighting, line numbers, and integrated editing.
2. **Interactive Terminal**: Implement a full xterm.js terminal that allows the user to manually run commands in the same environment as the agent.
3. **Live Preview**: Add a secondary pane to the UI that automatically renders HTML files or connects to a running dev server on a specific port.

## Phase 4: Scaling & Security (Day 9+)
*Goal: Prepare the system for more complex, multi-agent, or remote workflows.*

1. **Dockerized Execution**: Move the `workspace/` and `execute_command` logic into a Docker container to provide a completely isolated and secure sandbox.
2. **Multi-Agent Support**: Enable the main "Orchestrator" agent to spawn sub-agents for specific tasks (e.g., one for testing, one for documentation).
3. **Memory/Knowledge Base**: Integrate a vector database (like ChromaDB or Pinecone) to allow the agent to "remember" previous tasks and learn from past mistakes.

---

### Implementation Requirements for New Agents:
- **Requirement 1**: The agent must be able to edit specific lines of code without overwriting the entire file.
- **Requirement 2**: The agent must intelligently manage its context window, including "remembering" important project details while discarding redundant observations.
- **Requirement 3**: All new tools must include strict safety checks to prevent directory traversal or unauthorized system access.
