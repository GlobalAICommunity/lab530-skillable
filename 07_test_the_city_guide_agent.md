# Step 7: Test The City Guide Agent

In this exercise, you add knowledge to the workshop agent by testing a city guide
specialist in a separate file before wiring it into the main game agent. This
matters because guide missions should be solved with retrieval from the San
Francisco content instead of hard-coded answers or model guesses.

The specialist uses Foundry IQ to search a knowledge base backed by Azure AI
Search. Foundry IQ gives the agent relevant guide content at the moment it needs
it, so the model can answer from workshop material instead of relying only on
what it already knows. Keeping this retrieval logic in a specialist agent also
means the main game agent only spends search tokens when a guide question appears.

### In Microsoft Foundry, open the Foundry IQ setup:

1. In the top menu, select **Build**.
2. In the left menu, select **Knowledge**.
3. Scroll down until you see **Ground your agent in enterprise knowledge**.

Foundry IQ is backed by Azure AI Search. For this workshop, Azure AI Search is already
deployed; you only need to connect it to the Azure AI Search resource that was
created for the lab.

### In the Foundry IQ setup:

1. In the **Azure AI Search resource** dropdown, select the Azure AI Search
   resource. There should only be one option.
2. For **Auth Type**, select **API Key**.
3. Click **Create a knowledge base**.
4. 



Open the existing **.env** file. Confirm the city guide model deployment is
already set to **gpt-4.1-mini**, then add the Azure AI Search values:

```env
CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1-mini

AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_KNOWLEDGE_BASE_NAME=knowledgebase-city-guide
AZURE_SEARCH_KEY=<your-azure-ai-search-key>
```

The city guide specialist uses a smaller deployment than the main game agent.
Keep **CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME** set to **gpt-4.1-mini** so this
agent uses the city guide deployment you validated earlier.

In the VS Code Explorer, create a file named **agent_city_guide.py** in
**C:\workshop**. Paste the full code below into **agent_city_guide.py** and save
the file. This is the second specialist agent. Its search context provider lives
here, so the main game agent does not spend RAG tokens on every turn.

```python-notype
"""City guide specialist agent for San Francisco knowledge-base questions."""

import asyncio
import os

from agent_framework import Agent
from agent_framework.azure import AzureAISearchContextProvider
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv


def build_city_guide_agent():
	client = OpenAIChatClient(
		azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
		api_key=os.environ["AZURE_OPENAI_API_KEY"],
		model=os.environ["CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME"],
	)

	# Search context belongs here, so the main game agent does not spend RAG tokens on every turn.
	search_context_provider = AzureAISearchContextProvider(
		endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
		knowledge_base_name=os.environ["AZURE_SEARCH_KNOWLEDGE_BASE_NAME"],
		api_key=os.environ["AZURE_SEARCH_KEY"],
		mode="agentic",
	)

	guide_agent = Agent(
		client=client,
		name="San Francisco City Guide Agent",
		instructions=(
			"Answer San Francisco city guide questions using the provided search context. "
			"Keep answers brief and return only the answer needed by the game."
		),
		context_providers=[search_context_provider],
	)
	return guide_agent, search_context_provider


def build_city_guide_tool():
	guide_agent, search_context_provider = build_city_guide_agent()

	# The main game agent calls this tool only for city guide questions.
	guide_tool = guide_agent.as_tool(
		name="ask_city_guide",
		description=(
			"Ask the San Francisco city guide knowledge base a question. Use this only "
			"for city guide or local knowledge questions from the game."
		),
		arg_name="question",
		arg_description="The city guide question to answer.",
	)
	return guide_tool, search_context_provider


async def main() -> None:
	load_dotenv(override=True)

	question = "What neighborhood is Dolores Park in?"
	guide_agent, search_context_provider = build_city_guide_agent()

	try:
		response = await guide_agent.run(question)
		print(response.text)
	finally:
		await search_context_provider.close()


if __name__ == "__main__":
	asyncio.run(main())
```

Run **agent_city_guide.py** from the VS Code terminal:

```powershell
python agent_city_guide.py
```

> **Checkpoint:** the city guide agent should answer the Dolores Park question
> using the knowledge base. The answer should mention **Mission District**.

## What You Learned

You built and tested the city guide specialist that retrieves knowledge with
Foundry IQ before adding it to the main game agent.