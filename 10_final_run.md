# Final Run

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
