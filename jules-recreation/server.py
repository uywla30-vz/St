import os
import json
import asyncio
import aiofiles
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from agent import JulesAgent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Workspace path (using the jules-recreation/workspace directory)
WORKSPACE_DIR = os.path.abspath("./workspace")
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

agent = JulesAgent(WORKSPACE_DIR)

@app.get("/")
async def get():
    async with aiofiles.open("static/index.html", mode="r") as f:
        content = await f.read()
        return HTMLResponse(content=content)

@app.get("/api/files")
async def list_files():
    files = []
    for root, dirs, filenames in os.walk(WORKSPACE_DIR):
        for name in filenames:
            rel_path = os.path.relpath(os.path.join(root, name), WORKSPACE_DIR)
            files.append(rel_path)
    return {"files": files}

@app.get("/api/read")
async def read_file(path: str):
    full_path = os.path.join(WORKSPACE_DIR, path)
    if not os.path.abspath(full_path).startswith(WORKSPACE_DIR):
        return {"error": "Access denied"}
    try:
        async with aiofiles.open(full_path, mode="r") as f:
            content = await f.read()
            return {"content": content}
    except Exception as e:
        return {"error": str(e)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    async def agent_callback(type, msg):
        try:
            await websocket.send_json({"type": type, "message": msg})
        except Exception as e:
            print(f"Error sending to websocket: {e}")

    while True:
        try:
            data = await websocket.receive_text()
            task = json.loads(data).get("task")
            if task:
                await websocket.send_json({"type": "info", "message": f"Starting task: {task}"})
                await agent.run_task(task, agent_callback)
                await websocket.send_json({"type": "info", "message": "Task complete."})
        except Exception as e:
            print(f"WS connection closed or error: {e}")
            break

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
