# Step 3: Connect To The Gaming MCP Server

In this exercise, you connect the agent to the Lost in the City game server
through MCP so it can start sessions and call game actions as tools. This matters
because MCP turns the game into something the agent can operate instead of just
talking about.

The game exposes its actions as MCP tools. In the agent code this is the
`MCPStreamableHTTPTool` named `game_mcp`.

Open the existing **.env** file and confirm the game MCP URL is already there:

```env
GAME_MCP_URL=https://mcp.workshop.agentcon.dev/san-francisco/mcp
```

You do not need to change this value during the workshop.

Add the MCP imports:

```python
from agent_framework import Agent, MCPStreamableHTTPTool
```

Create and connect the tool before constructing the agent:

```python
game_mcp = MCPStreamableHTTPTool(
	name="Gaming MCP Server",
	url=os.environ["GAME_MCP_URL"],
)
await game_mcp.connect()
```

Pass it to the agent:

```python
agent = Agent(
	client=client,
	name="Game Play Agent",
	instructions=(
		"You are an agent that plays the game by using the available tools. "
		"Show story text returned by game tools in full. Keep your own extra commentary short and plain. "
		"Do not use markdown, bullet lists, tables, or code blocks. When a specialist tool returns advice "
		"or an answer, show it plainly before continuing."
	),
	tools=[game_mcp],
)
```

Create a chat session and start the game:

```python
session = agent.create_session()
response = await agent.run("start the game", session=session)
print(response.text)
```

Close the MCP connection at the end of `main()`:

```python
await game_mcp.close()
```

Run the agent from the VS Code terminal:

```powershell
python agent.py
```

Checkpoint: the agent should call the game server tools and receive a quest.
The first run usually registers a new player and starts a quest.

## What You Learned

You connected the agent to an MCP server, exposed the game actions as tools, and
started using the agent to interact with the game.

## Full agent.py Sample

If you want to compare your file with a complete version, **agent.py** should now
look like this:

```python
"""Game play agent using Microsoft Agent Framework, Azure OpenAI, and MCP."""

import asyncio
import os

from agent_framework import Agent, MCPStreamableHTTPTool
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv(override=True)


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
        agent = Agent(
            client=client,
            name="Game Play Agent",
            instructions=(
                "You are an agent that plays the game by using the available tools. "
                "Show story text returned by game tools in full. Keep your own extra "
                "commentary short and plain. Do not use markdown, bullet lists, "
                "tables, or code blocks. When a specialist tool returns advice or "
                "an answer, show it plainly before continuing."
            ),
            tools=[game_mcp],
        )

        session = agent.create_session()
        response = await agent.run("start the game", session=session)
        print(response.text)
    finally:
        await game_mcp.close()


if __name__ == "__main__":
    asyncio.run(main())
```
