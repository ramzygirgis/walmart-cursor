# AI Code Assistant (Gemini Agent)

This project implements a simple **in-terminal AI coding agent** inspired by tools like **Cursor** and **Claude Code**. The agent can inspect, edit, and run files inside a working directory in order to **diagnose and fix bugs automatically**.

The agent uses the **Gemini API** to reason about code and decide when to call tools that interact with the filesystem.

---

# Overview

The agent works by looping between the language model and a set of tools:

1. The user provides a prompt describing a task or bug.
2. The model reads the prompt and decides whether it needs to call a tool.
3. If a tool is needed (for example reading a file), the agent executes it.
4. The result is sent back to the model.
5. The model continues reasoning until it produces a final answer.

This is similar to the architecture used by modern **AI coding assistants**, where the model can:

* inspect files
* edit code
* run programs
* iterate until a fix is found

The main control loop for this process is implemented in `main.py`.

---

# Setup

## 1. Clone the repository

```bash
git clone https://github.com/ramzygirgis/walmart-cursor.git
cd walmart-cursor
```

---

## 2. Create and activate a virtual environment (recommended)

This project requires **Python 3.12 or newer**.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

---

## 3. Install dependencies

Dependencies are defined in **`pyproject.toml`**, so install them with:

```bash
pip install .
```

This will install the required packages:

- `google-genai`
- `python-dotenv`

---

## 4. Get a Gemini API Key

1. Go to:  
   https://aistudio.google.com/app/apikey

2. Create a new API key.

3. Copy the generated key.

---

## 5. Add the key to a `.env` file

Create a `.env` file in the root of the repository:

```env
GEMINI_API_KEY=your_api_key_here
```

The application automatically loads this key using **`python-dotenv`** when the program starts.


---

# Running the Agent

Example:

```
python main.py "Fix the bug in calculator/main.py"
```

Optional verbose mode:

```
python main.py "Fix the bug in calculator/main.py" --verbose
```

Verbose mode prints token usage for debugging and monitoring API usage.

---

# Rate Limits

Gemini free tier APIs have **small quotas**.

Common issues:

* `429 RESOURCE_EXHAUSTED`
* quota exceeded errors

Possible solutions:

* reduce `MAX_ITERATIONS`
* switch to a cheaper model such as:

```
gemini-2.0-flash
```

* wait for rate limits to reset
* enable billing for higher quotas

---

# How the Agent Fixes Bugs

The agent typically follows this workflow:

1. Explore the directory structure.
2. Read relevant source files.
3. Run the program to observe errors.
4. Modify files.
5. Re-run the program to test fixes.

This loop is repeated until the model believes the problem is solved.

---

# Future Improvements

Potential extensions for this project:

* add more tools (e.g. shell commands)
* add test running capabilities
* integrate with an editor
* implement memory or planning
* improve prompts and tool descriptions

---

## calculator/

A **sample project** used for testing the agent.

The agent can explore this directory, read files, modify them, and run Python code in order to debug issues.

This provides a safe environment to experiment with the agent’s capabilities.

---

## functions/

This directory contains the **tools available to the AI agent**.

Each tool performs a specific action inside the working directory.

---

### get_file_content.py

Reads the contents of a file.

Used when the model wants to inspect source code.

---

### get_files_info.py

Lists files and metadata within a directory.

Useful for discovering project structure.

---

### write_file.py

Writes or modifies files.

Allows the model to fix bugs or update code.

---

### run_python_file.py

Executes Python files inside the working directory.

This lets the model:

* run programs
* observe runtime errors
* test potential fixes

---

## call_function.py

Acts as the **bridge between the model and the tools**.

Responsibilities:

* registers the available tools (`available_functions`)
* interprets tool calls produced by the model
* executes the appropriate Python function
* returns the result to the model

This is what enables **function calling / tool use**.

---

## config.py

Contains configuration variables used by the agent, such as:

* Gemini model name
* maximum number of agent iterations
* maxmimum number of characters readable in a file


---


### Important

Gemini APIs have **fairly strict rate limits**, especially on the free tier.

If you encounter rate limit errors, you may need to **reduce `MAX_ITERATIONS`**.

Each iteration sends a request to the model.

---

## prompts.py

Contains the **system prompt** used by the agent.

This prompt defines:

* the agent’s role
* what tools it can use
* how it should reason about problems

Prompt design has a large impact on agent performance.

---

## main.py

This file contains the **core agent loop**.

High-level flow:

1. Load the Gemini API key.
2. Send the user prompt to the model.
3. The model decides whether to call a tool.
4. If a tool is requested:

   * execute it
   * return the result to the model
5. Repeat until the model produces a final response.

The loop runs for at most:

```
MAX_ITERATIONS
```

to prevent runaway execution.

---

## Tests

The repository includes several tests that verify the functionality of the tools:

```
test_get_file_content.py
test_get_files_info.py
test_run_python_file.py
test_write_file.py
```

These ensure that the tools behave correctly before they are exposed to the agent.

In the future these may be moved to a dedicated `tests/` directory.

---
