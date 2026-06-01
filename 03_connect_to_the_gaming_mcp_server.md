# Step 3: Connect To The Gaming MCP Server

In this exercise, you connect the agent to the Lost in the City game server
through MCP so it can start sessions and call game actions as tools. This matters
because MCP turns the game into something the agent can operate instead of just
talking about.

> [!Hint] 🖥️ **In VS Code** — this whole step happens in the VS Code editor and terminal.

The game exposes its actions as MCP tools and the game play agent prompt as an
MCP prompt. In the agent code this connection is the **MCPStreamableHTTPTool**
named **game_mcp**.

Open the existing **.env** file and confirm the game MCP URL is
already there:

```env
GAME_MCP_URL=https://mcp.workshop.agentcon.dev/san-francisco/mcp
```

You do not need to change this value during the workshop.

Go back to **agent.py**. At the top of **agent.py**, update the existing
Microsoft Agent Framework import so it also imports **MCPStreamableHTTPTool**:

```python
from agent_framework import Agent, MCPStreamableHTTPTool
```

Inside **main()**, create and connect the MCP tool after the Azure OpenAI client is
created and before the **Agent(...)** call:

```python
game_mcp = MCPStreamableHTTPTool(
	name="Gaming MCP Server",
	url=os.environ["GAME_MCP_URL"],
)
await game_mcp.connect()
```

> [!Hint] MCP servers can expose more than tools. They can also expose prompts
> that client agents load and use as instructions. In this workshop, the game
> server owns the game play prompt so the agent and game stay in sync.

After the MCP tool is connected, get the game play prompt from the MCP server:

```python
try:
    game_play_prompt = await game_mcp.get_prompt("game_play_prompt")
```

Still in **agent.py**,and inside the `try` block, update the existing **Agent(...)** call. Keep the client and name you already have, use **game_play_prompt** for the instructions, and add the
**tools=[game_mcp]** line:

```python
agent = Agent(
	client=client,
	name="Game Play Agent",
	instructions=game_play_prompt,
	tools=[game_mcp],
)
```

Create a chat session and start the game:

```python
session = agent.create_session()
response = await agent.run("start the game", session=session)
print(response.text)
```

Close the MCP connection at the end of **main()**:

```python
finally:
    await game_mcp.close()
```

Run the agent from the VS Code terminal:

```powershell
python agent.py
```

> **Checkpoint:** the terminal may show experimental warning messages from the
> framework, then the agent should welcome you to **Lost in San Francisco** and
> ask whether you already have a **player_id**. If you do not have one yet, it asks
> what name to put on your badge.

> [!Hint] Check for indentation if you run into errors. Python is identation
> sensitive, and as such you may run into runtime errors if blocks are not
> properly indented. Look at the Sample below if you need help with this.

## Full agent.py Sample

If you want to compare your file with a complete version, **agent.py** should now
look like this:

```python-notype
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
        game_play_prompt = await game_mcp.get_prompt("game_play_prompt")

        agent = Agent(
            client=client,
            name="Game Play Agent",
            instructions=game_play_prompt,
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

## What You Learned

You connected the agent to an MCP server, loaded the game play prompt from that
server, exposed the game actions as tools, and started using the agent to
interact with the game.