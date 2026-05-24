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

Still in **agent.py**, update the existing `Agent(...)` call. Keep the tools you
already have and add `agent42_tool` to the tools list:

```python
tools=[game_mcp, save_player_id, agent42_tool]
```

In the same `Agent(...)` call, update the instructions so the model knows when to
use Agent42:

```python
instructions=(
	"You are playing Lost in San Francisco. Use game tools to begin or resume "
	"the session. Save any returned player_id. For movement missions, ask "
	"Agent42 for the best transport option, then submit Agent42's recommendation "
	"as the mission answer."
)
```

Checkpoint: during the first movement mission, the session log should show a
call to `ask_agent42` before `submit_mission_answer`.

## What You Learned

You exposed Agent42 as a tool so the main agent can delegate movement decisions
to a specialist agent during the game.
