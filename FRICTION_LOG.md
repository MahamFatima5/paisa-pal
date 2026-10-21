# Friction Log

This log records the problems I hit while building Paisa Pal with the MCP Python SDK, Streamlit, and related tools during the hackathon. Each entry lists the task, steps, expected vs actual result, severity, workaround, and a suggestion.

---

## 1. Starting the MCP server from a tutorial

- **Task:** Create an MCP server with a `FastMCP` class, as shown in common tutorials.
- **Steps:** Wrote `from mcp.server.fastmcp import FastMCP` and ran `mcp dev mcp_server/server.py`.
- **Expected:** The server starts and the Inspector connects.
- **Actual:** `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`. The installed `mcp` was 2.x, where `FastMCP` was renamed to `MCPServer`.
- **Severity:** High (blocked the start of the project)
- **Workaround:** Changed the import to `from mcp.server.mcpserver import MCPServer` and the class name to `MCPServer`.
- **Suggestion:** Show the version in the first line of every tutorial, and add a migration note on the docs home page for the rename.

## 2. Inspector showed an old server entry

- **Task:** Test the tools in MCP Inspector.
- **Steps:** Ran `mcp dev mcp_server/server.py` after the server was fixed.
- **Expected:** Inspector shows only the server I started.
- **Actual:** Inspector listed a server called `uv` that I did not create, which timed out after 30 seconds.
- **Severity:** Medium (confusing, but did not block the work)
- **Workaround:** Installed `uv`, restarted Inspector, and used the correct server entry.
- **Suggestion:** Show which command or config a server entry came from, and let users remove stale entries from the UI.

## 3. Streamable HTTP client function name and return values

- **Task:** Write a Python client that calls the server over Streamable HTTP.
- **Steps:** Imported `streamablehttp_client` from `mcp.client.streamable_http`, then unpacked three values from it.
- **Expected:** The import and unpacking match the docs.
- **Actual:** First an `ImportError` (the name is `streamable_http_client`), then `ValueError: not enough values to unpack (expected 3, got 2)`. It returns only `read` and `write`.
- **Severity:** High (blocked the chat UI until fixed)
- **Workaround:** Listed the module's names with `dir()`, then changed the import and unpacking.
- **Suggestion:** Put a complete Streamable HTTP client example in the docs that matches the current version.

## 4. Port 8000 already in use

- **Task:** Start the MCP server on port 8000 after restarting VS Code.
- **Steps:** Ran `python mcp_server/server.py` in a new terminal.
- **Expected:** Server starts at `http://127.0.0.1:8000`.
- **Actual:** `[Errno 10048] error while attempting to bind on address`. An old server process was still running.
- **Severity:** Medium
- **Workaround:** Used `netstat -ano | findstr :8000` to find the process ID, then `taskkill /PID <id> /F`.
- **Suggestion:** Print a clear message when the port is busy, with the command to free it, and support a `PORT` environment variable.

## 5. Broken uvicorn and websockets install

- **Task:** Start the Streamable HTTP server.
- **Steps:** Ran `python mcp_server/server.py` after a normal install.
- **Expected:** Uvicorn starts.
- **Actual:** `SyntaxError: source code string cannot contain null bytes` inside the `websockets` package.
- **Severity:** High (blocked the server until fixed)
- **Workaround:** Ran `pip install --force-reinstall --no-cache-dir websockets uvicorn`.
- **Suggestion:** Pin tested versions of uvicorn and websockets in the MCP dependencies, so fresh installs do not break.

## 6. Hosting limits on free plans

- **Task:** Deploy the MCP server to a free host so judges can open the chat online.
- **Steps:** Created a Render web service and selected the Free instance type.
- **Expected:** Deploy on the free plan without a card.
- **Actual:** A payment form asked for a card, and free instances spin down after inactivity, with no persistent disk.
- **Severity:** Medium (live demo was not deployed)
- **Workaround:** Ran the project locally and documented the local setup steps in the README.
- **Suggestion:** Make the free tier's card requirement and limits clear before the deploy form, and support a free persistent option for demo apps.
