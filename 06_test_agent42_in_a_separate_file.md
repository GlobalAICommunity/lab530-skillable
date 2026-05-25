# Step 6: Test Agent42 In A Separate File

In this exercise, you test Agent42 in a separate file before wiring it into the
main game agent. This matters because Agent42 is the transport expert, and a
standalone smoke test helps confirm A2A communication works before the full game
flow depends on it.

Open the existing **.env** file and confirm the deployed Agent42 A2A
URL is already present:

```env
AGENT42_URL=https://agent42.workshop.agentcon.dev/
```

> [!Hint] A2A stands for Agent-to-Agent. It lets one agent expose itself to
> another agent as a callable specialist. In this step, your main workshop code
> connects to Agent42 over A2A so it can ask transport questions and receive a
> structured recommendation.

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

Run **agent_agent42.py** from the VS Code terminal:

```powershell
python agent_agent42.py
```

> **Checkpoint:** Agent42 replies with route options and ends with lines like:

```text
recommendation: car
recommendation code: <code>
```

## What You Learned

You connected to another agent through the A2A protocol and tested Agent42 as a
standalone transport specialist before adding it to the main agent.
