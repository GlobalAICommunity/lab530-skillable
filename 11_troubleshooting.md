# Troubleshooting

| Symptom | Check |
| --- | --- |
| `KeyError: AZURE_OPENAI_ENDPOINT` | **my-agent/.env** is missing or not loaded. |
| `KeyError: GAME_MCP_URL` | Add the deployed game MCP URL to **my-agent/.env**. |
| MCP connection fails | Confirm `GAME_MCP_URL` is the deployed MCP endpoint and includes `/san-francisco/mcp`. |
| Agent keeps registering new players | Confirm **my-agent/memory.json** exists and contains `player_id`. |
| Agent42 tool fails | Confirm `AGENT42_URL` is the deployed A2A endpoint and includes `https://`. |
| Guide question is guessed | Confirm `ask_city_guide` is in the main agent tools, `AZURE_SEARCH_KEY` is set, and the session log shows a call to `ask_city_guide`. |
| Tool choice is confusing | Open the latest file in `logs` from the VS Code Explorer and inspect `MODEL INPUT`, `TOOL CALL`, and `TOOL RESULT` entries. |
