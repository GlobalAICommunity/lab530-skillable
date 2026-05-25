# Step 6: Test Agent42 Transport Specialist

In this exercise, you test Agent42 in a separate file before wiring it into the
main game agent. This matters because movement missions in the game ask the
agent to choose between options like **car**, **walking**, and **bike**. Agent42
is the transport specialist: it can compare a route, consider live weather and
traffic, and return a recommendation the game agent can use before submitting a
mission answer. A standalone smoke test helps confirm A2A communication works
before the full game flow depends on it.

Open the existing **.env** file and confirm the deployed Agent42 A2A
URL is already present:

```env
AGENT42_URL=https://agent42.workshop.agentcon.dev/
```

> [!Hint] A2A stands for Agent-to-Agent. It lets one agent call another agent as
> a specialist instead of rebuilding that specialist's logic locally. In this
> step, **agent_agent42.py** connects to the deployed Agent42 service, sends it a
> transport question, and gets back route advice that the main game agent can use
> later.

In the VS Code Explorer, create a file named **agent_agent42.py** in
**C:\workshop**. Paste the full code below into **agent_agent42.py** and save the
file. This file keeps the Agent42 A2A setup out of the main game agent, and it
gives you a small smoke test you can run by itself:

```python-notype
"""Agent42 transport specialist tool for movement missions."""

import asyncio
import os

from agent_framework.a2a import A2AAgent
from dotenv import load_dotenv


def build_agent42_agent():
	# Agent42 is a deployed A2A agent. The URL comes from .env.
	return A2AAgent(
		name="Agent42",
		description=(
			"Local transport expert. Given an origin and destination, recommends "
			"car/taxi vs walking vs bike using live weather and real-time traffic, "
			"and returns a static map of the chosen route plus a recommendation code."
		),
		url=os.environ["AGENT42_URL"],
	)


def build_agent42_tool():
	agent42 = build_agent42_agent()

	# The main game agent calls this tool for movement quests.
	return agent42.as_tool(
		name="ask_agent42",
		description=(
			"Ask Agent42 for the best way to get from one place to another. "
			"Pass a full natural-language question including origin, destination."
		),
		arg_name="question",
		arg_description="The transport question to send to Agent42.",
	)


async def main() -> None:
	load_dotenv(override=True)

	question = "What is the best way to get from the Ferry Building to Golden Gate Park?"
	response = await build_agent42_agent().run(question)
	print(response.text)


if __name__ == "__main__":
	asyncio.run(main())
```

> [!Hint] You can experiment by editing the `question = "What is the best way to
> get from the Ferry Building to Golden Gate Park?"` line. Choose two places that
> are close enough for **car**, **bike**, and **walking** to all be plausible. Keep
> them within about **50 km** of each other so Agent42 can show its reasoning.

Run **agent_agent42.py** from the VS Code terminal:

```powershell
python agent_agent42.py
```

> **Checkpoint:** Agent42 should compare the route options and recommend one
> transport choice. The reply should include a map link; Ctrl-click the link to
> open it and inspect the route on the map. The reply should look like this:

```text-notype-nocopy
Weather: 12°C, overcast

Options:
Car: 4.3 miles, 16 minutes + 5 minutes pickup wait
Bike: 4.0 miles, 20 minutes
Walking: 3.7 miles, 72 minutes

Reasoning: Car is the best balance of speed and convenience here, even after adding the rideshare pickup wait. It's cool and overcast, so biking is still fine, but it takes longer than driving. Walking is a pretty long trek for this trip.

map: https://lab530storage.blob.core.windows.net/agent42-routes/w55nhqthcqzimgl.png
directions: https://lab530storage.blob.core.windows.net/agent42-routes/w55nhqthcqzimgl.json
recommendation: car
recommendation code: w55nhqthcqzimgl
```

## What You Learned

You connected to another agent through the A2A protocol and tested Agent42 as a
standalone transport specialist before adding it to the main agent.
