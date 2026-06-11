# Lost in the City Agent Workshop

> [!Hint] 🖥️ **In VS Code** — you'll do all of this lab's hands-on work in VS Code, except where a step tells you to switch to the browser.

## The Story

You've just landed in Rio de Janeiro, Brazil. The afternoon heat hangs over Guanabara
Bay, your phone is almost dead, and somewhere across the city — past the
arches of Lapa, the crowds of Copacabana, and the slopes below Corcovado —
there's a final destination waiting. The clock is ticking.

You won't be navigating alone. In this workshop you'll build an AI **player
agent** that takes on the *Lost in the City* quest on your behalf. It will:

- Pick up missions from a game server and report back the answers.
- Phone a transport expert, **Agent42**, to decide whether to grab a taxi,
   hop on a bike, or hoof it — based on the weather, traffic, and route.
- Consult a **city guide** knowledge base to dig clues out of Rio de
   Janeiro's neighborhoods, history, food, and hidden corners.
- Remember who the player is between runs, and write a clear log of every
   model call, tool call, and decision it made.

Whoever's agent solves the most missions, fastest, takes the leaderboard.

## What You'll Build

A single Python agent, built with the **Microsoft Agent Framework**, that
combines four capabilities you'll add one step at a time:

- **MCP (Model Context Protocol)** — connect to the game server to start
   quests, submit answers, and progress through missions.
- **A2A (Agent-to-Agent)** — call Agent42 as a peer agent for
   weather-aware transport recommendations.
- **Knowledge retrieval** — query an Azure AI Search knowledge base over the Rio
   de Janeiro city guide to answer the trivia-style missions.
- **Memory & logging** — remember the player ID between runs and capture
   every prompt, tool call, and response in a session log you can inspect.

By the end you'll have a working agent that plays the game end-to-end, and
you'll have seen how the framework, MCP, A2A, and retrieval fit together in
a real application instead of a toy demo.


## Login into the Machine
Everything you'll do today happens on the Windows 11 lab VM on the left
of your screen - browser, code editor, terminal, the lot. Sign in once
and you're set for the rest of the workshop. Click inside the VM,
unlock it, and use the credentials below:

**Password**: +++@lab.VirtualMachine(Win11-Pro-Base).Password+++


## Step Into Your Workspace

On the Windows desktop, click the **Visual Studio Code** icon to open VS Code.

When VS Code starts, the **C:\workshop** folder should already be open. If that is
not the case:

1. Select **File > Open Folder**.
2. Choose the **C:\workshop** directory.

Open the integrated terminal with **Terminal > New Terminal** and confirm the
terminal is PowerShell and the prompt is inside **C:\workshop**.

The workshop environment already has the required Python packages installed. 

If you want to verify the packages from the VS Code terminal, run:

```powershell
python -c "import agent_framework, dotenv; print('workshop packages ready')"
```

The **C:\workshop** folder already has a **.env** file. You do not need to create a new
one. As you go through the workshop, open that file and add the values needed
for the current step.

## What You Learned

You confirmed the workshop workspace, terminal, installed packages, and **.env**
file are ready before building the agent.
