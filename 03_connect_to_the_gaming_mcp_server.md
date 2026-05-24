# Step 3: Connect To The Gaming MCP Server

The game exposes its actions as MCP tools. In the agent code this is the
`MCPStreamableHTTPTool` named `game_mcp`.

Open the existing `.env` file and add the deployed game MCP URL:

```env
GAME_MCP_URL=https://<deployed-game-host>/san-francisco/mcp
```

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
		"You are playing Lost in San Francisco. Use the game tools to begin "
		"or resume a session, register when needed, start the quest, and submit "
		"mission answers."
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

Checkpoint: the agent should call the game server tools and receive a quest.
The first run usually registers a new player and starts a quest.

## What You Learned

You connected the agent to an MCP server, exposed the game actions as tools, and
started using the agent to interact with the game.
