# Claude-CLI-Agent

A **tool-using LLM agent** that executes terminal commands, reads/writes files, and automates tasks — built in Python with OpenAI Claude models.

This project explores **autonomous AI agents** that integrate **LLMs with external tools** to perform real-world tasks from the command line.

---

## 🚀 Project Overview

Claude-CLI-Agent demonstrates:

- LLM reasoning over tasks in natural language.
- Safe execution of terminal commands.
- File I/O operations via AI instructions.
- Context-aware workflows with tool-call tracking.

It is implemented as a **single Python CLI script** leveraging OpenAI Claude APIs.

---

## 🧩 Features (Mapped to Code)

| Feature                     | How it works in code                                                            |
| --------------------------- | ------------------------------------------------------------------------------- |
| **CLI interaction**         | Uses `argparse` to accept user prompts (`-p "<your command>"`)                  |
| **Read files**              | `"Read"` tool implemented in code: opens files and returns content to the agent |
| **Write files**             | `"Write"` tool: appends content to files safely                                 |
| **Execute shell commands**  | `"Bash"` tool: runs commands via `subprocess.run` and captures output           |
| **Tool calls tracking**     | Messages appended with `tool_call_id` for each tool invocation                  |
| **Context-aware reasoning** | `msgs` array keeps full conversation and tool call history for multi-step tasks |
| **Error handling**          | Checks for empty API responses and captures command errors via `stderr`         |

---

## 🏗️ Architecture

```text
User Prompt
    |
    v
+----------------+
| LLM Reasoning  |
+----------------+
        |
        v
+----------------+       +----------------+       +----------------+
| Read Tool      |       | Write Tool     |       | Bash Tool      |
+----------------+       +----------------+       +----------------+
        ^                       ^                       ^
        |                       |                       |
        +------- Execution Feedback & Tool Responses --+
```

- **LLM Reasoning**: Uses Claude-Haiku-4.5 (`client.chat.completions.create`) to interpret user instructions.
- **Read/Write Tools**: File operations via JSON tool calls (`Read`, `Write`).
- **Bash Tool**: Executes shell commands safely, returning stdout/stderr.
- **Conversation Context**: Stored in `msgs` and passed back to LLM for multi-step reasoning.

---

## 🔧 Installation

1. Clone the repository:

```bash
git clone https://github.com/GeoNjunge/Claude-CLI-Agent.git
cd Claude-CLI-Agent
```

2. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set environment variables:

```bash
export OPENROUTER_API_KEY="your_api_key"
export OPENROUTER_BASE_URL="https://openrouter.ai/api/v1"  # optional, default included
```

---

## ⚡ How to Run

```bash
python app/main.py -p "List all files in this directory"
```

The agent will:

1. Send the prompt to the Claude model.
2. Evaluate the task.
3. Call the appropriate tool (`Read`, `Write`, or `Bash`) automatically.
4. Return the results to the CLI.

Example:

```bash
$ python claude_agent.py -p "Create a file called test.txt and write 'Hello World'"
Claude-CLI-Agent: Running `Write` -> success
```

---

## 🧠 Key Learnings

- Integrating LLMs with **tool-based actions**.
- Maintaining **conversation context** for multi-step reasoning.
- Safe execution of system commands with **subprocess**.
- File I/O operations via AI tool calls.
- CLI design for autonomous AI interactions.

---

## 💡 Future Work

- Add **multi-agent coordination** for more complex workflows.
- Enhance **tool safety** checks (prevent dangerous commands).
- Add **logging & metrics** for agent decision tracking.
- Integrate **web or GUI interface** for remote interaction.

---

## 📝 License

MIT — free to use, modify, and extend.
