# Step 9: Add The City Guide Tool To The Main Agent

In this exercise, you add the city guide specialist as a tool on the main game
agent. This matters because the final agent needs both movement advice from
Agent42 and local knowledge from the city guide to complete the full quest.

Go back to **agent.py**. At the top of **agent.py**, with the other imports,
import the city guide builder from **agent_city_guide.py**:

```python
from agent_city_guide import build_city_guide_tool
```

Inside `main()`, create the city guide tool after the Agent42 tool and before the
`Agent(...)` call:

```python
guide_tool, city_guide_search = build_city_guide_tool()
```

Still in **agent.py**, update the existing `Agent(...)` call. Keep `game_mcp`,
`save_player_id`, and `agent42_tool` from the previous steps, then add
`guide_tool` to the tools list:

```python
tools=[game_mcp, save_player_id, agent42_tool, guide_tool]
```

In the same `Agent(...)` call, keep the main agent context providers focused on
memory only:

```python
context_providers=[
	PlayerContextProvider(source_id="player-memory"),
]
```

At the end of `main()`, close both long-lived resources. Keep the existing
`game_mcp.close()` call and add `city_guide_search.close()` next to it:

```python
await game_mcp.close()
await city_guide_search.close()
```

In the same `Agent(...)` call, keep `instructions=game_play_prompt`. The game
play prompt still comes from the MCP server.

```python
instructions=game_play_prompt
```

The Azure AI Search context provider lives inside **agent_city_guide.py**, not in
the main game agent. That means search is only loaded when the main agent calls
`ask_city_guide`, instead of spending RAG tokens on every game turn.

> **Checkpoint:** during the guide question, the session log should show a call
> to `ask_city_guide`. The city guide model input should include retrieved guide
> context.

## What You Learned

You added the city guide specialist as an on-demand tool, so the main agent only
uses knowledge retrieval when the game needs local guide information.
