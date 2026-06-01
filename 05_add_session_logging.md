# Step 5: Add Session Logging

In this exercise, you add session logging so you can inspect what the agent sent,
what the model returned, and which tools were called. This matters because agent
behavior is much easier to debug when each model call and tool result is visible.

> [!Hint] 🖥️ **In VS Code** — this whole step happens in the VS Code editor and terminal.

First, create the logging helper file. In the VS Code Explorer, click the new
file button, name the file **log.py**, and make sure it appears next to
**agent.py** in **C:\workshop**. Paste the full helper code below into
**log.py** and save the file.

This helper records user turns, model input, tool calls, and tool results. You
will not run **log.py** directly. The main **agent.py** file will import and use
these helper functions.

```python-notype
"""Per-session conversation and tool logging for the workshop agent."""
from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from agent_framework import agent_middleware, chat_middleware, function_middleware

LOGS_DIR = Path(__file__).resolve().parent / "logs"


def open_session_log() -> Path:
	LOGS_DIR.mkdir(exist_ok=True)
	stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
	path = LOGS_DIR / f"session-{stamp}-{uuid.uuid4().hex[:6]}.log"
	path.write_text(f"# Session log started {datetime.now().isoformat()}\n\n")
	return path


def _append(path: Path, header: str, body: str) -> None:
	ts = datetime.now().strftime("%H:%M:%S")
	with path.open("a", encoding="utf-8") as file:
		file.write(f"[{ts}] {header}\n{body.rstrip()}\n\n")


def _truncate(text: str, limit: int = 4000) -> str:
	if len(text) <= limit:
		return text
	return text[:limit] + f"\n... [truncated {len(text) - limit} chars]"


def _stringify(value: Any) -> str:
	try:
		return json.dumps(value, indent=2, default=str, ensure_ascii=False)
	except Exception:
		return repr(value)


def _format_messages(messages) -> str:
	parts: list[str] = []
	for message in messages or []:
		role = getattr(message, "role", "?")
		text = "".join(
			(getattr(content, "text", "") or "")
			for content in getattr(message, "contents", []) or []
		)
		if text:
			parts.append(f"[{role}] {text}")
	return "\n".join(parts)


def build_logging_middleware(log_path: Path):
	@agent_middleware
	async def log_agent(context, call_next):
		text = _format_messages(context.messages)
		if text:
			_append(log_path, "USER ->", _truncate(text))

		await call_next()

		result = getattr(context, "result", None)
		out = getattr(result, "text", None)
		if out:
			_append(log_path, "AGENT <-", _truncate(out))

	@chat_middleware
	async def log_chat(context, call_next):
		text = _format_messages(context.messages)
		if text:
			_append(log_path, "MODEL INPUT (post context providers) ->", _truncate(text))
		await call_next()

	@function_middleware
	async def log_function(context, call_next):
		function_name = getattr(getattr(context, "function", None), "name", "?")
		arguments = getattr(context, "arguments", {}) or {}
		_append(log_path, f"TOOL CALL  {function_name}", _truncate(_stringify(arguments)))

		await call_next()

		result = getattr(context, "result", None)
		_append(log_path, f"TOOL RESULT {function_name}", _truncate(_stringify(result)))

	return log_agent, log_chat, log_function
```

> [!Hint] **What is middleware?**
> Middleware is a function that wraps a step in the agent's pipeline so you can run code before and after it. The **await call_next()** line is what actually executes the step — anything before it runs first, anything after runs once the step completes. This framework has three interception points: the full agent turn **@agent_middleware**, the model call **@chat_middleware**, and each tool call **@function_middleware**. Here you are using all three to write a log entry at each stage.

Now go back to **agent.py**. At the top of **agent.py**, with the other imports,
import the two helper functions from **log.py**:

```python
from log import build_logging_middleware, open_session_log
```

Next, stay in **agent.py** and find the **main()** function. Inside **main()**, add
the logging setup after the MCP tool is connected and before the **Agent(...)** is
created:

```python-notype
log_path = open_session_log()
print(f"Session log: {log_path}")
agent_mw, chat_mw, function_mw = build_logging_middleware(log_path)
```

This creates a new file in the **logs** folder for the current run and builds the
three middleware functions that will write to it.

Finally, still in **agent.py**, update the existing **Agent(...)** call. Keep the
tools and context provider you already added, and add the **middleware** line shown
below:

```python-notype
agent = Agent(
	client=client,
	name="Game Play Agent",
	instructions=game_play_prompt,
	tools=[game_mcp, save_player_id],
	context_providers=[PlayerContextProvider(source_id="player-memory")],
	middleware=[agent_mw, chat_mw, function_mw],
)
```

Because Step 4 saved your **player_id** in **memory.json**, you no longer need
to send your name in code. Still inside **main()**, remove these two lines:

```python
response = await agent.run("My name is <Your Name>", session=session)
print(response.text)
```

## Full agent.py Sample

If you want to compare your file with a complete version, **agent.py** should now
look like this:

```python-notype
"""Game play agent using Microsoft Agent Framework, Azure OpenAI, and MCP."""

import asyncio
import json
import os
from pathlib import Path

from agent_framework import Agent, ContextProvider, MCPStreamableHTTPTool, tool
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv
from log import build_logging_middleware, open_session_log

MEMORY_FILE = Path("memory.json")

load_dotenv(override=True)


class PlayerContextProvider(ContextProvider):
	async def before_run(self, *, agent, session, context, state) -> None:
		if MEMORY_FILE.exists():
			pid = json.loads(MEMORY_FILE.read_text()).get("player_id")
			if pid:
				context.extend_instructions(
					self.source_id,
					f"From memory: player_id: {pid}",
				)


@tool(description="Save the player_id returned after registration")
async def save_player_id(player_id: str) -> str:
	MEMORY_FILE.write_text(json.dumps({"player_id": player_id}))
	return f"Player ID {player_id} saved."


async def main() -> None:
	client = OpenAIChatClient(
		azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
		api_key=os.environ["AZURE_OPENAI_API_KEY"],
		model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
	)

	game_mcp = MCPStreamableHTTPTool(
		name="Gaming MCP Server",
		url=os.environ["GAME_MCP_URL"],
	)
	await game_mcp.connect()

	try:
		game_play_prompt = await game_mcp.get_prompt("game_play_prompt")
		log_path = open_session_log()
		print(f"Session log: {log_path}")
		agent_mw, chat_mw, function_mw = build_logging_middleware(log_path)

		agent = Agent(
			client=client,
			name="Game Play Agent",
			instructions=game_play_prompt,
			tools=[game_mcp, save_player_id],
			context_providers=[PlayerContextProvider(source_id="player-memory")],
			middleware=[agent_mw, chat_mw, function_mw],
		)

		session = agent.create_session()
		response = await agent.run("start the game", session=session)
		print(response.text)

	finally:
		await game_mcp.close()


if __name__ == "__main__":
	asyncio.run(main())
```

Run **agent.py** again from the VS Code terminal:

```powershell
python agent.py
```

The terminal should print a line that starts with **Session log:**. Because the
previous step saved your **player_id** in **memory.json**, the agent should find
that player in memory and resume instead of asking you to register again.

In the VS Code Explorer, open the **logs** folder and select the newest log file.
Read through the log to see what happened: the saved **player_id** is added to
the model context, the agent calls the game MCP tools, and the tool results are
recorded for inspection.

> **Checkpoint:** the **logs** folder contains a new session log file for the
> latest run. The file shows the saved **player_id** from memory, the model
> input, the game MCP tool calls, the tool results, and the final response.

## What You Learned

You added middleware that records user turns, model input, tool calls, and tool
results so you can inspect how the agent made each decision.
