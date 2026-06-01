# Lab Recap

You built a working player agent for the **Lost in the City** workshop. The
agent can start or resume a game, choose tools, ask other services for help,
retrieve guidebook knowledge, remember useful state, and log what happened.

> [!Hint] 📖 **Just reading** — this recap has no hands-on steps; nothing to switch to.

## What You Built

- A Python agent using the Microsoft Agent Framework.
- A connection to the game server through MCP.
- A memory file that keeps the player ID between runs.
- Session logging so you can inspect model input, model output, tool calls,
   and tool results.
- A separate Agent42 test client for transport recommendations.
- An Agent42 tool inside the main player agent.
- A city guide specialist that answers questions from the San Francisco guide.
- A city guide tool inside the main player agent.
- A final run that plays through the complete quest.

## How The Pieces Fit Together

The game server owns the quest state and exposes missions through MCP. Your
player agent decides what to do next and calls tools when it needs outside help.

Agent42 acts as a transport expert. When the game asks how to move through the
city, your agent asks Agent42 for a recommendation and submits that answer back
to the game server.

The city guide agent acts as a retrieval specialist. When the game asks a
guidebook question, your agent calls the guide tool, finds the relevant city
knowledge, and submits the answer.

Memory keeps the same player session alive across runs. Logging lets you see
why the agent made each decision.

## What To Take Away

- MCP is useful when an agent needs to work with an external app or game state.
- A2A is useful when one agent should ask another agent for specialized help.
- Retrieval helps the agent answer questions from a trusted knowledge source.
- Memory turns repeated runs into a continued session instead of a fresh start.
- Logging makes agent behavior easier to debug, explain, and improve.

## Next Steps

- Try another run and compare the session log with what happened in the game.
- Change the agent instructions and see how the tool choices change.
- Add another small tool to the player agent.
- Extend the city guide with more source material.
- Reuse the same MCP, A2A, retrieval, memory, and logging pattern in your own
   agent project.