# Step 4: Add Memory For The Player ID

The game returns a `player_id`. The agent needs to save it so future runs can
resume the same game.

Add imports:

```python
import json
from pathlib import Path

from agent_framework import ContextProvider, tool
```

Add the memory file constant near the top of the file:

```python
MEMORY_FILE = Path("memory.json")
```

Inside `main()`, add a context provider that injects the saved player ID before
each model run:

```python
class PlayerContextProvider(ContextProvider):
	async def before_run(self, *, agent, session, context, state) -> None:
		if MEMORY_FILE.exists():
			pid = json.loads(MEMORY_FILE.read_text()).get("player_id")
			if pid:
				context.extend_instructions(
					self.source_id,
					f"From memory: player_id: {pid}",
				)
```

Add a tool the model can call after registration:

```python
@tool(description="Save the player_id returned after registration")
async def save_player_id(player_id: str) -> str:
	MEMORY_FILE.write_text(json.dumps({"player_id": player_id}))
	return f"Player ID {player_id} saved."
```

Register the memory provider and memory tool:

```python
agent = Agent(
	client=client,
	name="Game Play Agent",
	instructions=(
		"You are playing Lost in San Francisco. When a player_id is returned, "
		"call save_player_id. If memory provides a player_id, resume that player."
	),
	tools=[game_mcp, save_player_id],
	context_providers=[PlayerContextProvider(source_id="player-memory")],
)
```

Checkpoint: after registration, **C:\workshop\memory.json** should contain the saved
`player_id`. On the next run, the agent should resume instead of registering a
new player.

## What You Learned

You added lightweight memory with a context provider and a save tool so the
agent can remember its `player_id` between runs.
