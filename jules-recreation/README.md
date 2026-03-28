# Jules Recreation

This is a functional recreation of the Jules AI agent platform, inspired by `jules.google.com`. It features an autonomous AI agent capable of managing a local workspace through a web-based interface.

## Features
- **Autonomous Agent**: Uses a Thought-Action-Observation loop to solve tasks.
- **Real-time Terminal**: Streams the agent's internal reasoning and command outputs via WebSockets.
- **File Explorer**: Browse files created or modified by the agent in the dedicated workspace.
- **Code Viewer**: Inspect file contents directly in the browser.
- **Local Tooling**: The agent can list, read, write, and execute shell commands within its workspace.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn huggingface_hub python-dotenv aiofiles websockets
   ```

2. **Configure API Token**:
   Create a `.env` file in the `jules-recreation` directory and add your Hugging Face token (with Inference API permissions):
   ```env
   HF_TOKEN=your_token_here
   ```

3. **Run the Server**:
   ```bash
   python server.py
   ```

4. **Access the UI**:
   Open your browser and navigate to `http://localhost:8000`.

## Architecture
- `agent.py`: Contains the `JulesAgent` class, which manages the LLM interaction and tool execution.
- `server.py`: A FastAPI server that handles the web interface, file APIs, and WebSocket communication.
- `static/`: Contains the frontend assets (HTML, CSS, JS).
- `workspace/`: The dedicated directory where the agent operates.

## Security Note
The agent is restricted to operating within the `workspace/` directory. However, because it can execute shell commands, it should be used in a trusted environment.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
