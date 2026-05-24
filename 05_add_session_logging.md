# Step 5: Add Session Logging

In this exercise, you add session logging so you can inspect what the agent sent,
what the model returned, and which tools were called. This matters because agent
behavior is much easier to debug when each model call and tool result is visible.

First, create the logging helper file. In the VS Code Explorer, click the new
file button, name the file **log.py**, and make sure it appears next to
**agent.py** in **C:\workshop**. Paste the full helper code below into
**log.py** and save the file.

This helper records user turns, model input, tool calls, and tool results. You
will not run **log.py** directly. The main **agent.py** file will import and use
these helper functions.

```python
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

Now go back to **agent.py**. At the top of **agent.py**, with the other imports,
import the two helper functions from **log.py**:

```python
from log import build_logging_middleware, open_session_log
```

Next, stay in **agent.py** and find the `main()` function. Inside `main()`, add
the logging setup after the MCP tool is connected and before the `Agent(...)` is
created:

```python
log_path = open_session_log()
print(f"Session log: {log_path}")
agent_mw, chat_mw, function_mw = build_logging_middleware(log_path)
```

This creates a new file in the **logs** folder for the current run and builds the
three middleware functions that will write to it.

Finally, still in **agent.py**, update the existing `Agent(...)` call. Keep the
tools and context provider you already added, and add the `middleware` line shown
below:

```python
agent = Agent(
	client=client,
	name="Game Play Agent",
	instructions="...",
	tools=[game_mcp, save_player_id],
	context_providers=[PlayerContextProvider(source_id="player-memory")],
	middleware=[agent_mw, chat_mw, function_mw],
)
```

Checkpoint: run **agent.py** again. The terminal should print a line that starts
with `Session log:`. In the VS Code Explorer, open the **logs** folder and select
the newest log file. Use that file when the agent makes a surprising tool choice,
because it shows the model input, tool calls, tool results, and final response.

## What You Learned

You added middleware that records user turns, model input, tool calls, and tool
results so you can inspect how the agent made each decision.
