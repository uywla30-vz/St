import os
import json
import asyncio
import re
from typing import List, Dict, Any, Callable
from huggingface_hub import AsyncInferenceClient
from dotenv import load_dotenv

load_dotenv()

class JulesAgent:
    def __init__(self, root_dir: str):
        self.root_dir = os.path.abspath(root_dir)
        self.client = AsyncInferenceClient(
            model="Qwen/Qwen2.5-Coder-32B-Instruct",
            token=os.getenv("HF_TOKEN")
        )
        self.system_prompt = f"""You are Jules, an expert AI coding agent.
Your goal is to assist the user by performing tasks within the local directory: {self.root_dir}.

You operate in a Thought-Action-Observation loop.
1. **Thought**: Explain what you are going to do and why.
2. **Action**: Call a tool to perform an action.
3. **Observation**: The result of the action.

Available Tools:
- `list_files(path=".")`: Lists files in a directory.
- `read_file(filepath)`: Reads the content of a file.
- `write_file(filepath, content)`: Creates or overwrites a file.
- `execute_command(command)`: Runs a shell command.

IMPORTANT:
- Stay within {self.root_dir}. Do not attempt to access or modify files outside this directory.
- Use valid JSON for tool calls.
- ONLY ONE tool call per response is allowed. Do not include multiple ACTION: blocks.
- When you are finished, state "FINAL_ANSWER: [summary of what you did]".

Format tool calls like this:
ACTION: {{"tool": "tool_name", "parameters": {{"param1": "value1"}}}}
"""

    def _safe_path(self, path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.root_dir, path))
        if not full_path.startswith(self.root_dir):
            raise PermissionError(f"Access denied: {path} is outside the root directory.")
        return full_path

    def list_files(self, path: str = ".") -> str:
        safe_path = self._safe_path(path)
        try:
            files = os.listdir(safe_path)
            return json.dumps(files)
        except Exception as e:
            return str(e)

    def read_file(self, filepath: str) -> str:
        safe_path = self._safe_path(filepath)
        try:
            with open(safe_path, "r") as f:
                return f.read()
        except Exception as e:
            return str(e)

    def write_file(self, filepath: str, content: str) -> str:
        safe_path = self._safe_path(filepath)
        try:
            os.makedirs(os.path.dirname(safe_path), exist_ok=True)
            with open(safe_path, "w") as f:
                f.write(content)
            return f"Successfully wrote to {filepath}"
        except Exception as e:
            return str(e)

    async def execute_command(self, command: str) -> str:
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.root_dir
            )
            stdout, stderr = await process.communicate()
            return f"STDOUT: {stdout.decode()}\nSTDERR: {stderr.decode()}"
        except Exception as e:
            return str(e)

    async def run_task(self, task: str, callback: Callable[[str, str], Any]):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": task}
        ]

        for _ in range(15):  # Max 15 steps
            response = ""
            try:
                resp = await self.client.chat_completion(
                    messages=messages,
                    max_tokens=2048
                )
                response = resp.choices[0].message.content
            except Exception as e:
                await callback("error", f"Model error: {str(e)}")
                break

            await callback("thought", response)
            messages.append({"role": "assistant", "content": response})

            if "FINAL_ANSWER:" in response:
                break

            # Parse Action using a balanced brace approach
            if "ACTION:" in response:
                try:
                    action_start = response.find("ACTION:") + 7
                    json_text = response[action_start:].strip()

                    # Find balanced braces
                    brace_count = 0
                    first_brace = -1
                    last_brace = -1
                    for i, char in enumerate(json_text):
                        if char == '{':
                            if brace_count == 0:
                                first_brace = i
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                last_brace = i
                                break

                    if first_brace != -1 and last_brace != -1:
                        action_json = json_text[first_brace:last_brace+1]
                        action = json.loads(action_json)
                    tool_name = action["tool"]
                    params = action.get("parameters", {})

                    observation = ""
                    if tool_name == "list_files":
                        observation = self.list_files(**params)
                    elif tool_name == "read_file":
                        observation = self.read_file(**params)
                    elif tool_name == "write_file":
                        observation = self.write_file(**params)
                    elif tool_name == "execute_command":
                        observation = await self.execute_command(**params)
                    else:
                        observation = f"Unknown tool: {tool_name}"

                    await callback("observation", observation)
                    messages.append({"role": "user", "content": f"OBSERVATION: {observation}"})
                except Exception as e:
                    error_msg = f"Error parsing/executing action: {str(e)}"
                    await callback("error", error_msg)
                    messages.append({"role": "user", "content": error_msg})
            else:
                if "FINAL_ANSWER:" not in response:
                    prompt = "Please proceed with the next step or provide a FINAL_ANSWER."
                    messages.append({"role": "user", "content": prompt})

if __name__ == "__main__":
    # Simple CLI test
    import asyncio
    async def simple_callback(type, msg):
        print(f"[{type.upper()}] {msg}")

    workspace = "./test_workspace"
    if not os.path.exists(workspace):
        os.makedirs(workspace)

    agent = JulesAgent(workspace)
    asyncio.run(agent.run_task("Create a hello.py file that prints 'Hello from Async Jules!' and then run it.", simple_callback))
