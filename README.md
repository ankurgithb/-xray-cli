
A modular Python CLI chat assistant built to inspect how LLM chat APIs work under the hood—separating **persisted application history** from the **sliding model context window**, toggling **stateless mode**, and exposing token usage and raw API payloads on demand.

---

## Features

- **Application State vs. Model Context:** Persists full chat history on disk (`chat_history.json`) while sending only a configurable sliding window (`MAX_CONTEXT_MESSAGES`) to the API.
- **Stateless Toggle (`/stateless`):** Switch off conversation memory mid-session to observe how LLMs behave when only the current prompt is sent.
- **Context Inspector (`/context`):** Compare total saved history messages against the exact slice sent in the API payload.
- **On-Demand Telemetry (`/usage` & `/raw`):** Keep chat turns clean while inspecting token counts (`prompt_tokens`, `completion_tokens`, `total_tokens`), finish reasons, or the full raw JSON response whenever needed.
- **Safe Error Rollback:** Automatically removes unsent user messages from history if an API request fails.

---

## Architecture & Project Structure

```text
xray-CLI/
├── .env               # API key and model configuration (not committed)
├── config.py          # Environment loader, system prompt, and context/token limits
├── state_manager.py   # Disk persistence and sliding-window context builder
├── telemetry.py       # Response metadata and token usage formatter
└── main.py            # Interactive CLI loop and slash command handlers
```

### How It Works

1. **User Input:** `main.py` captures user input and appends it to local history via `state_manager.py`.
2. **Context Slicing:** `build_model_context()` slices either the most recent `MAX_CONTEXT_MESSAGES` (default `6`) or only the latest message if `/stateless` is enabled.
3. **Payload Assembly:** `main.py` prepends `INSTRUCTIONS` as the `system` message and sends the payload to Groq's OpenAI-compatible Chat Completions endpoint (`https://api.groq.com/openai/v1`).
4. **Persistence & Inspection:** The assistant reply is saved to disk and printed cleanly, while the full response object remains cached in memory for `/usage` or `/raw`.

---

## Setup & Installation

### 1. Install Dependencies

```bash
pip install openai python-dotenv
```

### 2. Configure Environment Variables

Create a `.env` file in the root of `xray-CLI/`:

```env
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

### 3. Run the CLI

```bash
python3 -u main.py
```

---

## CLI Commands

| Command | Description |
| :--- | :--- |
| `/context` | Show total persisted messages vs. messages currently sent in the model context window. |
| `/stateless` | Toggle stateless mode (`True`/`False`) to test single-turn requests without history. |
| `/usage` | Display model name, finish reason, and token counts (`input`, `output`, `total`) for the last turn. |
| `/raw` | Print the complete raw JSON response from the most recent API call. |
| `/reset` | Clear conversation history in memory and on disk. |
| `/exit` | Exit the CLI. |

---

## Core Concepts Demonstrated

- **LLMs Are Stateless:** Conversation memory is an application-layer pattern created by re-sending prior `user` and `assistant` messages on each turn.
- **Input Token Growth:** As conversation turns accumulate within `MAX_CONTEXT_MESSAGES`, `prompt_tokens` increases with every request until older messages slide out of the window.
- **Application State vs. Model Context:** What your app stores on disk can be arbitrarily long, while what the model sees is strictly bounded by your context window policy.
