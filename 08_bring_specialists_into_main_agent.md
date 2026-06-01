# Step 8: Bring The Specialist Agents Into The Main Agent

In this exercise, you add Agent42 and the city guide specialist to the main game
agent, then run the complete chat loop. This matters because the final agent
needs the game MCP tools, memory, logging, transport advice, and retrieval all
working together in one conversation.

> [!Hint] 🖥️ **In VS Code** — this whole step happens in the VS Code editor and terminal.

Go back to **agent.py**. At the top of **agent.py**, with the other imports,
import the two specialist tool builders:

```python
from agent_agent42 import build_agent42_tool
from agent_city_guide import build_city_guide_tool
```

Inside **main()**, create the specialist tools after the game MCP server is
connected and before the **Agent(...)** call:

```python
agent42_tool = build_agent42_tool()
guide_tool, city_guide_search = build_city_guide_tool()
```

Still in **agent.py**, update the existing **Agent(...)** call. Keep **game_mcp**
and **save_player_id** from the previous steps, then add **agent42_tool** and
**guide_tool** to the tools list:

```python
tools=[game_mcp, save_player_id, agent42_tool, guide_tool]
```

In the same **Agent(...)** call, keep the main agent context providers focused on
memory only:

```python
context_providers=[PlayerContextProvider(source_id="player-memory")]
```

At the end of **main()**, close both long-lived resources. Keep the existing
**game_mcp.close()** call and add **city_guide_search.close()** next to it:

```python
await game_mcp.close()
await city_guide_search.close()
```

Finally, replace the single **agent.run(...)** call with a chat loop so you can
keep playing after the first game response:

```python
print("Chat with Game Play Agent (type 'exit' or 'quit' to stop)\n")
session = agent.create_session()
response = await agent.run("start the game", session=session)
print(f"Agent: {response.text}\n")

while True:
	try:
		user_input = input("You: ").strip()
	except (EOFError, KeyboardInterrupt):
		print()
		break
	if not user_input:
		continue
	if user_input.lower() in {"exit", "quit"}:
		break
	response = await agent.run(user_input, session=session)
	print(f"Agent: {response.text}\n")
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
from agent_city_guide import build_city_guide_tool
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

	city_guide_search = None
	try:
		game_play_prompt = await game_mcp.get_prompt("game_play_prompt")
		log_path = open_session_log()
		print(f"Session log: {log_path}")
		agent_mw, chat_mw, function_mw = build_logging_middleware(log_path)
		agent42_tool = build_agent42_tool()
		guide_tool, city_guide_search = build_city_guide_tool()

		agent = Agent(
			client=client,
			name="Game Play Agent",
			instructions=game_play_prompt,
			tools=[game_mcp, save_player_id, agent42_tool, guide_tool],
			context_providers=[PlayerContextProvider(source_id="player-memory")],
			middleware=[agent_mw, chat_mw, function_mw],
		)

		print("Chat with Game Play Agent (type 'exit' or 'quit' to stop)\n")
		session = agent.create_session()
		response = await agent.run("start the game", session=session)
		print(f"Agent: {response.text}\n")

		while True:
			try:
				user_input = input("You: ").strip()
			except (EOFError, KeyboardInterrupt):
				print()
				break
			if not user_input:
				continue
			if user_input.lower() in {"exit", "quit"}:
				break
			response = await agent.run(user_input, session=session)
			print(f"Agent: {response.text}\n")
	finally:
		await game_mcp.close()
		if city_guide_search:
			await city_guide_search.close()


if __name__ == "__main__":
	asyncio.run(main())
```

Run the complete agent from the VS Code terminal:

```powershell
python agent.py
```

Expected flow:

1. The agent starts or resumes a game session.
2. It saves or reuses the **player_id**.
3. It calls **ask_agent42** for movement missions.
4. It calls **ask_city_guide** for guide questions.
5. It reaches the final destination and appears on the leaderboard.

> **Checkpoint:** the terminal shows the final game result, and the session log
> contains calls to the game MCP tools, **ask_agent42**, and **ask_city_guide**.

## What You Learned

You brought the specialist agents into the main game agent, added an interactive
chat loop, and ran the complete Lost in the City flow end to end.