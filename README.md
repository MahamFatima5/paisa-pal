# Paisa Pal

Paisa Pal is an expense tracker you control in plain language. Type "chai pe 300 kharch kiye" and an MCP server saves it. Ask for a monthly summary and it totals your spending by category.

## Built during the Amazon Developer Hackathon (Alexa+ track)

- MCP server in Python (`mcp_server/server.py`) with tools `add_expense` and `monthly_summary`, served over Streamable HTTP (MCP spec 2025-11-25).
- Streamlit chat UI (`chat_app.py`) that calls the MCP server.
- HTTP test client (`test_client.py`).

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install "mcp[cli]" streamlit
```

## Run

Terminal 1, start the MCP server:

```bash
python mcp_server/server.py
```

Terminal 2, start the chat UI:

```bash
streamlit run chat_app.py
```

Open http://localhost:8501 and try "chai pe 300 kharch kiye" or "is mahine ka summary do".

## License

MIT

##Demo Video

Demo video: https://youtu.be/j2zK8mdmNXo
