# Schoology MCP Dashboard

A beautiful web dashboard for the [Schoology MCP](https://github.com/dajun666/schoology-mcp) server, giving you AI-powered access to your PAUSD Schoology grades, assignments, courses, and more.

![Schoology Help Dashboard](https://img.shields.io/badge/Platform-PAUSD%20Schoology-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![License](https://img.shields.io/badge/License-MIT-purple)

## Features

- **AI Study Assistant** - Chat with DeepSeek AI about your grades, assignments, and courses
- **Real-time Grades** - View all your course grades with category breakdowns
- **Assignment Tracking** - See upcoming due dates and never miss a deadline
- **Activity Feed** - Latest posts from your teachers
- **Markdown Support** - Rich text, code blocks, LaTeX math, tables
- **Image Analysis** - Upload images and extract text via OCR
- **Demo Mode** - Try it immediately without any setup

## Quick Start (Demo Mode)

No setup required! Just open `index.html` in your browser and click **"Try Demo Mode"**.

## Full Setup (for real Schoology data)

### Step 1: Clone the Repository

```bash
git clone https://github.com/dajun666/schoology-mcp.git
cd schoology-mcp
```

### Step 2: Run the Setup Script

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install dependencies (Flask, Playwright, etc.)
- Install Chromium browser for Playwright

### Step 3: Configure Your Credentials

Edit the `.env` file:
```bash
nano .env
```

Set your PAUSD student ID:
```
SCHOOLOGY_USERNAME=12345678
```

### Step 4: Store Your Password

```bash
source .venv/bin/activate
python scripts/set_credentials.py
```

Enter your Schoology password when prompted. It will be stored securely in your OS keychain (not in any file).

### Step 5: Test the Login

```bash
python scripts/login_check.py
```

This will open a browser, log into Schoology, and verify everything works.

### Step 6: Start the Server

```bash
source .venv/bin/activate
python server.py
```

Then open [http://localhost:8080](http://localhost:8080) in your browser.

### Step 7: Configure AI (Optional)

To use the AI assistant, deploy the DeepSeek proxy worker and enter the worker URL in the Settings tab.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Your Browser                                  │
│                    (index.html - Dashboard)                          │
└─────────────────────────────────────────────────────────────────────┘
                                 │
                                 ▼ HTTP / REST
┌─────────────────────────────────────────────────────────────────────┐
│                   Frontend Server (server.py)                       │
│                      localhost:8080                                 │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐  │
│  │  Grades    │  │  Courses    │  │ Assignments │  │ AI Chat    │  │
│  │  Endpoint  │  │  Endpoint   │  │  Endpoint   │  │  Endpoint  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
              │                                    │
              ▼ (if MCP installed)                 ▼ (if DeepSeek Worker configured)
┌─────────────────────────────┐      ┌─────────────────────────────┐
│     Schoology MCP Server     │      │    DeepSeek AI Proxy       │
│   (schoology-mcp/server.py)  │      │  (Cloudflare Worker)       │
│         + Playwright        │      │                            │
└─────────────────────────────┘      └─────────────────────────────┘
              │
              ▼
┌─────────────────────────────┐
│      PAUSD Schoology        │
│   pausd.schoology.com      │
└─────────────────────────────┘
```

## Files

```
schoologyhelp/
├── index.html          # Web dashboard (open directly or via server)
├── server.py           # Python Flask server (optional, for API bridging)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── schoology-mcp/      # Cloned Schoology MCP repository
    ├── server.py       # MCP server
    ├── setup.sh        # Setup script
    └── ...
```

## Security

- Your Schoology password is stored in your OS keychain, never in plaintext
- The agent password (`sb250wocaonimalegebide`) protects access to this tool
- Session data is git-ignored and never committed

## Troubleshooting

### Login fails
```bash
# Check if Chrome/Chromium is installed
playwright install chromium

# Test login manually
python scripts/login_check.py --show-browser
```

### AI not working
1. Deploy your DeepSeek proxy worker to Cloudflare
2. Copy the worker URL
3. Paste it in the Settings tab of the dashboard

### Port already in use
```bash
# Change port in server.py
app.run(host='0.0.0.0', port=8081, debug=True)
```

## License

MIT - Fork it and customize for your district!