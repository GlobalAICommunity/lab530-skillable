# Step 8: Test The City Guide Agent

The second mission is a city-guide question. The workshop knowledge base has
already been created from the city-guide content so the agent can retrieve the
answer without hard-coding it.

In Microsoft Foundry:

1. Create or open the workshop project.
2. Open the knowledge base named `knowledgebase-city-guide`.
3. Confirm it is backed by Azure AI Search.
4. Copy the Azure AI Search endpoint and query/admin key.

Open the existing `.env` file and add the city guide model deployment plus the
Azure AI Search values:

```env
CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME=<your-city-guide-deployment>

AZURE_SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
AZURE_SEARCH_KNOWLEDGE_BASE_NAME=<your-knowledge-base-name>
AZURE_SEARCH_KEY=<your-azure-ai-search-key>
```

The city guide specialist can use a smaller or cheaper deployment than the main
game agent. If you want to keep the setup simple, set
`CITY_GUIDE_AZURE_OPENAI_DEPLOYMENT_NAME` to the same deployment name as
`AZURE_OPENAI_DEPLOYMENT_NAME`.

Create `agent_city_guide.py`. This is a second specialist agent. Its search
context provider lives here, so the main game agent does not spend RAG tokens on
every turn.

```python
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

Run it from the VS Code terminal:

```powershell
python agent_city_guide.py
```

Checkpoint: the city guide agent should answer the Dolores Park question using
the knowledge base.

## What You Learned

You built a city guide specialist that retrieves knowledge with Foundry IQ and
keeps the search context outside the main game agent.
