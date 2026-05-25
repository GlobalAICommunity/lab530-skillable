# Step 7: Add Agent42 To The Main Agent

In this exercise, you add Agent42 to the main game agent so movement missions can
use transport advice before submitting an answer. This matters because the game
expects choices like `car`, `walking`, or `bike`, and the main agent should ask a
specialist instead of guessing.

Go back to **agent.py**. At the top of **agent.py**, with the other imports,
import the builder from **agent_agent42.py**:

```python
from agent_agent42 import build_agent42_tool
```

Inside `main()`, create the Agent42 tool after the game MCP server is connected
and before the `Agent(...)` call:

```python
agent42_tool = build_agent42_tool()
```

Still in **agent.py**, update the existing `Agent(...)` call. Keep `game_mcp`
and `save_player_id` from the previous steps, and add `agent42_tool` to the
tools list:

```python
tools=[game_mcp, save_player_id, agent42_tool]
```

## Full agent.py Sample

If you want to compare your file with a complete version, **agent.py** should now
look like this:

```python-notype
"""Game play agent using Microsoft Agent Framework with Azure OpenAI."""

import asyncio
import json
import os
from pathlib import Path

from agent_agent42 import build_agent42_tool
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
		log_path = open_session_log()
		print(f"Session log: {log_path}")
		agent_mw, chat_mw, function_mw = build_logging_middleware(log_path)
		agent42_tool = build_agent42_tool()

		agent = Agent(
			client=client,
			name="Game Play Agent",
			instructions=(
				"You are playing Lost in San Francisco. When a player_id is returned, "
				"call save_player_id. If memory provides a player_id, resume that player."
			),
			tools=[game_mcp, save_player_id, agent42_tool],
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

> **Checkpoint:** during the first movement mission, the session log should show
> a call to `ask_agent42` before `submit_mission_answer`.

## What You Learned

You exposed Agent42 as a tool so the main agent can delegate movement decisions
to a specialist agent during the game.
