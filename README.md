# AI Coding Agent

A CLI-based AI agent powered by Google's Gemini API that can autonomously complete coding tasks by reasoning through problems and using tools to interact with a local codebase.

## What it does

You give it a prompt, it figures out what needs to happen, and it gets to work. The agent runs in a loop — up to 20 iterations — calling tools, reading results, and adjusting its approach until it has a final answer for you.

Under the hood it's working against a real Python calculator project (`./calculator`), so it has actual files to read, run, and modify.

## How it works

The agent follows a straightforward cycle each iteration:

1. Send the conversation history to Gemini 2.5 Flash
2. If the model wants to call a tool, execute it and feed the result back
3. If the model has a final response, print it and stop
4. If 20 iterations pass with no resolution, exit with an error

The model always sees the full conversation — every prior response and every tool result — so it can reason across multiple steps without losing context.

## Tools available to the agent

| Tool | What it does |
|---|---|
| `get_files_info` | List files and directories with sizes |
| `get_file_content` | Read a file's contents (truncated at a max character limit) |
| `run_python_file` | Execute a Python file and capture stdout/stderr |
| `write_file` | Write or overwrite a file, creating directories as needed |

Each tool is sandboxed to the working directory — the agent can't read or write outside of it.

## Usage

```bash
python main.py "your prompt here"
python main.py "your prompt here" --verbose
```

`--verbose` prints each function call with its arguments and the result it returned.

## Setup

```bash
cp .env.example .env  # add your GEMINI_API_KEY
uv sync
```

## Tech

- Python 3.12
- [Google GenAI SDK](https://pypi.org/project/google-genai/) (`google-genai`)
- Gemini 2.5 Flash