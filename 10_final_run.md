# Final Run

In this exercise, you run the complete agent end to end and watch it play through
the full Lost in the City flow. This matters because it confirms the model
connection, MCP tools, memory, logging, Agent42, and city guide retrieval all work
together as one agent.

Run the complete agent from the VS Code terminal:

```powershell
python agent.py
```

Expected flow:

1. The agent starts or resumes a game session.
2. It saves or reuses the `player_id`.
3. It asks Agent42 for the first movement mission.
4. It submits the transport recommendation to the MCP game server.
5. It calls `ask_city_guide` for the guide question.
6. It asks Agent42 again for the final movement mission.
7. It reaches Fort Mason and appears on the leaderboard.

## What You Learned

You ran the completed agent through the full quest and confirmed that the model
connection, MCP tools, memory, logging, Agent42, and city guide retrieval work
together in one end-to-end flow.
