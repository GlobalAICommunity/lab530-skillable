# Step 4: Add Memory For The Player ID

In this exercise, you add lightweight memory so the agent can save the
`player_id` returned by the game. This matters because future runs should resume
the same player session instead of registering a new player every time.

Go back to **agent.py**. At the top of **agent.py**, add these imports with the
other imports:

```python
import json
from pathlib import Path

from agent_framework import ContextProvider, tool
```

In **agent.py**, add the memory file constant near the top of the file, after the
imports and before `load_dotenv(override=True)`:

```python
MEMORY_FILE = Path("memory.json")
```

> [!Hint] A context provider is a small hook that runs before the model gets a
> turn. It can add useful context to the agent instructions, such as remembered
> state from a previous run. In this step, the context provider reads
> **memory.json** and tells the agent which `player_id` to resume.

In **agent.py**, add this context provider class after the memory file constant
and before `main()`. It injects the saved player ID before each model run:

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

> [!Hint] Tool calling lets the model ask your Python code to do a specific
> action. The model decides when the tool is needed, passes arguments to it, and
> receives the tool result back in the conversation. In this step, the tool gives
> the agent a controlled way to save the `player_id` after the game registers a
> player.

In **agent.py**, add this tool function below the context provider class. The
model can call it after registration to save the player ID:

```python
@tool(description="Save the player_id returned after registration")
async def save_player_id(player_id: str) -> str:
	MEMORY_FILE.write_text(json.dumps({"player_id": player_id}))
	return f"Player ID {player_id} saved."
```

Inside `main()`, update the existing `Agent(...)` call. Keep
`instructions=game_play_prompt` and the game MCP tool, then add both the memory
tool and context provider:

```python
agent = Agent(
	client=client,
	name="Game Play Agent",
	instructions=game_play_prompt,
	tools=[game_mcp, save_player_id],
	context_providers=[PlayerContextProvider(source_id="player-memory")],
)
```

> **Checkpoint:** after registration, **C:\workshop\memory.json** should contain the saved
> `player_id`. On the next run, the agent should resume instead of registering a
> new player.

## What You Learned

You added lightweight memory with a context provider and a save tool so the
agent can remember its `player_id` between runs.
