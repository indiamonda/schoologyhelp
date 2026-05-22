# Schoology MCP Frontend

A web-based dashboard for the [Schoology MCP](https://github.com/dajun666/schoology-mcp) server.

## Files

- `index.html` - Frontend web interface (single-page app)
- `server.py` - Python Flask backend that bridges frontend to MCP server
- `requirements.txt` - Python dependencies
- `integrate.py` - Demo script showing MCP protocol integration

## Setup

```bash
pip install -r requirements.txt
python server.py
```

Open http://localhost:8080

## Architecture

The frontend (index.html) communicates with the Flask server (server.py) via REST API.
The Flask server acts as a proxy to the actual Schoology MCP server.

To connect to a real MCP server, update `integrate.py` with the correct path
and register it with Claude Code using:
```bash
claude mcp add schoology -- /path/to/.venv/bin/python /path/to/server.py
```