# Step 9: Add The City Guide Tool To The Main Agent

In `agent.py`, import the city guide builder:

```python
from agent_city_guide import build_city_guide_tool
```

Create the city guide tool after the Agent42 tool:

```python
guide_tool, city_guide_search = build_city_guide_tool()
```

Add it to the tools list:

```python
tools=[game_mcp, save_player_id, agent42_tool, guide_tool]
```

Keep the main agent context providers focused on memory only:

```python
context_providers=[
	PlayerContextProvider(source_id="player-memory"),
]
```

Close both long-lived resources at the end of `main()`:

```python
await game_mcp.close()
await city_guide_search.close()
```

Update the instructions one last time:

```python
instructions=(
	"You are an agent that plays the game by using the available tools. "
	"Show story text returned by game tools in full. Keep your own extra commentary short and plain. "
	"Do not use markdown, bullet lists, tables, or code blocks. When a specialist tool returns advice "
	"or an answer, show it plainly before continuing."
)
```

The Azure AI Search context provider lives inside `agent_city_guide.py`, not in
the main game agent. That means search is only loaded when the main agent calls
`ask_city_guide`, instead of spending RAG tokens on every game turn.

Checkpoint: during the guide question, the session log should show a call to
`ask_city_guide`. The city guide model input should include retrieved guide
context.

## What You Learned

You added the city guide specialist as an on-demand tool, so the main agent only
uses knowledge retrieval when the game needs local guide information.
