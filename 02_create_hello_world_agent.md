# Step 2: Create A Hello-World Agent

In this exercise, you create the smallest possible Microsoft Agent Framework
agent so you can prove the model connection works. This matters because a simple
hello-world run gives you a clean baseline before MCP, memory, A2A, and retrieval
add more moving parts.

> [!Hint] 🖥️ **In VS Code** — this whole step happens in the VS Code editor and terminal.

In the VS Code Explorer, create a file named **agent.py** in **C:\workshop**.
Paste the full code below into **agent.py** and save the file:

```python-notype
"""Game play agent using Microsoft Agent Framework with Azure OpenAI."""

import asyncio
import os

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv(override=True)


async def main() -> None:
	client = OpenAIChatClient(
		azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
		api_key=os.environ["AZURE_OPENAI_API_KEY"],
		model=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
	)

	agent = Agent(
		client=client,
		name="Game Play Agent",
		instructions="You are a friendly workshop agent. Reply briefly.",
	)

	response = await agent.run("Say hello to the workshop.")
	print(response.text)


if __name__ == "__main__":
	asyncio.run(main())
```

Run **agent.py** from the VS Code terminal:

```powershell
python agent.py
```

> **Checkpoint:** the terminal prints a short hello from the model.

## What You Learned

You created a minimal Microsoft Agent Framework agent, connected it to Azure
OpenAI, and made your first model call from **agent.py**.
