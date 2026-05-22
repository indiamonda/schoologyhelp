# Schoology MCP Frontend

A web dashboard for the [Schoology MCP](https://github.com/dajun666/schoology-mcp) server that provides a visual interface to access your PAUSD Schoology grades, assignments, courses, and recent posts.

## Features

- **Dashboard** - Overview of grades, upcoming assignments, and recent activity
- **Grades** - Detailed view of current grades by course with category breakdown
- **Courses** - List of enrolled courses with teacher and room info
- **Assignments** - Upcoming assignments sorted by due date
- **Recent Posts** - Latest activity feed from teachers
- **Settings** - Configure server connection and trigger manual sync

## Quick Start

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

### 2. Configure the Backend Server

```bash
mkdir -p ~/.schoology-mcp
cp .env.example ~/.schoology-mcp/.env
# Edit .env with your student ID
```

### 3. Start the Frontend Server

```bash
python server.py
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  Frontend Server │────▶│  Schoology MCP  │
│   (index.html)  │     │   (server.py)    │     │   (server.py)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │                         │
                              │  REST API               │  MCP Protocol
                              │  /api/grades            │  get_grades
                              ▼                         ▼
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard HTML |
| `/health` | GET | Health check |
| `/api/grades` | GET | Get current grades |
| `/api/courses` | GET | Get enrolled courses |
| `/api/assignments` | GET | Get upcoming assignments |
| `/api/posts` | GET | Get recent activity posts |
| `/api/refresh` | POST | Force refresh all data |
| `/api/clear-session` | POST | Clear Schoology session |
| `/api/config` | GET/POST | Get/set configuration |
| `/api/status` | GET | Get connection status |

## Configuration

Settings are stored in `~/.schoology-mcp/config.json` and can be configured through the Settings panel in the web interface.

## License

MIT