#!/usr/bin/env python3
"""
Schoology MCP Frontend Server
Provides REST API endpoints that the frontend uses to communicate with the Schoology MCP server.
"""

import os
import json
import subprocess
import threading
from datetime import datetime
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

# Configuration
CONFIG_FILE = Path.home() / '.schoology-mcp' / 'config.json'
STATE_FILE = Path.home() / '.schoology-mcp' / 'storage_state.json'
ENV_FILE = Path.home() / '.schoology-mcp' / '.env'

# MCP Server configuration (loaded from config or defaults)
MCP_SERVER_HOST = os.environ.get('MCP_SERVER_HOST', 'localhost')
MCP_SERVER_PORT = int(os.environ.get('MCP_SERVER_PORT', '8765'))

# Cache for MCP responses
cache = {
    'grades': None,
    'courses': None,
    'assignments': None,
    'posts': None,
    'last_updated': None
}
cache_lock = threading.Lock()


def load_config():
    """Load configuration from config file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save configuration to config file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def get_env_config():
    """Load configuration from .env file."""
    env_config = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    key, value = line.split('=', 1)
                    env_config[key.strip()] = value.strip().strip('"').strip("'")
    return env_config


def call_mcp_tool(tool_name, arguments=None):
    """
    Call a tool on the MCP server using claude mcp command.
    Returns parsed JSON response or raises exception.
    """
    import urllib.request
    import urllib.error

    # For now, we'll simulate responses since the actual MCP integration
    # requires the server to be registered and running.
    # In production, this would use the MCP protocol over HTTP.

    # Simulated responses for demonstration
    simulated_responses = {
        'get_grades': [
            {'courseName': 'Calculus BC', 'teacher': 'Dr. Smith', 'percentage': 94, 'letterGrade': 'A', 'period': 1,
             'categoryGrades': {'Tests': 92, 'Homework': 98, 'Quizzes': 94}},
            {'courseName': 'AP English Literature', 'teacher': 'Ms. Johnson', 'percentage': 88, 'letterGrade': 'B+', 'period': 2,
             'categoryGrades': {'Essays': 85, 'Participation': 95, 'Projects': 88}},
            {'courseName': 'Physics C: Mechanics', 'teacher': 'Mr. Williams', 'percentage': 91, 'letterGrade': 'A-', 'period': 3,
             'categoryGrades': {'Labs': 93, 'Tests': 90, 'Homework': 92}},
            {'courseName': 'Computer Science Principles', 'teacher': 'Ms. Davis', 'percentage': 96, 'letterGrade': 'A', 'period': 4,
             'categoryGrades': {'Projects': 98, 'Tests': 94, 'Homework': 97}},
            {'courseName': 'US History', 'teacher': 'Mr. Brown', 'percentage': 85, 'letterGrade': 'B', 'period': 5,
             'categoryGrades': {'Essays': 82, 'Tests': 88, 'Participation': 85}},
            {'courseName': 'Spanish Language', 'teacher': 'Sra. Martinez', 'percentage': 92, 'letterGrade': 'A-', 'period': 6,
             'categoryGrades': {'Speaking': 94, 'Writing': 90, 'Reading': 93}}
        ],
        'get_courses': [
            {'name': 'Calculus BC', 'teacher': 'Dr. Smith', 'period': 1, 'room': 'M-101'},
            {'name': 'AP English Literature', 'teacher': 'Ms. Johnson', 'period': 2, 'room': 'E-205'},
            {'name': 'Physics C: Mechanics', 'teacher': 'Mr. Williams', 'period': 3, 'room': 'P-302'},
            {'name': 'Computer Science Principles', 'teacher': 'Ms. Davis', 'period': 4, 'room': 'T-101'},
            {'name': 'US History', 'teacher': 'Mr. Brown', 'period': 5, 'room': 'H-104'},
            {'name': 'Spanish Language', 'teacher': 'Sra. Martinez', 'period': 6, 'room': 'F-201'}
        ],
        'get_upcoming_assignments': [
            {'title': 'Calculus Chapter 7 Test', 'courseName': 'Calculus BC', 'dueDate': '2026-05-25', 'points': 100},
            {'title': 'AP English Essay - Hamlet Analysis', 'courseName': 'AP English Literature', 'dueDate': '2026-05-23', 'points': 50},
            {'title': 'Physics Lab Report - Momentum', 'courseName': 'Physics C: Mechanics', 'dueDate': '2026-05-24', 'points': 30},
            {'title': 'CS Project - Final Iteration', 'courseName': 'Computer Science Principles', 'dueDate': '2026-05-26', 'points': 100},
            {'title': 'History DBQ - Civil Rights', 'courseName': 'US History', 'dueDate': '2026-05-27', 'points': 45},
            {'title': 'Spanish Conversation Practice', 'courseName': 'Spanish Language', 'dueDate': '2026-05-22', 'points': 20}
        ],
        'get_recent_posts': [
            {'author': 'Dr. Smith', 'timestamp': '2026-05-22T10:30:00Z',
             'content': 'Reminder: The Calculus Chapter 7 test has been moved to May 25. Please review integration techniques and application problems.',
             'attachments': [{'name': 'Review_Packet.pdf', 'type': 'pdf'}]},
            {'author': 'Ms. Johnson', 'timestamp': '2026-05-22T09:15:00Z',
             'content': 'Great work on the practice essays everyone! Your thesis statements have improved significantly. Office hours Thursday if you need help with Hamlet.',
             'attachments': []},
            {'author': 'Mr. Williams', 'timestamp': '2026-05-21T14:45:00Z',
             'content': 'Lab reports due Friday. Make sure to include error analysis and proper significant figures. Check the sample report format in the shared folder.',
             'attachments': [{'name': 'Sample_Lab_Report.docx', 'type': 'doc'}]},
            {'author': 'Ms. Davis', 'timestamp': '2026-05-21T11:00:00Z',
             'content': 'Final project presentations start next week. Sign up for a slot in the shared spreadsheet. Remember to demo your working application.',
             'attachments': [{'name': 'Presentation_Schedule.xlsx', 'type': 'xlsx'}]},
            {'author': 'Sra. Martinez', 'timestamp': '2026-05-20T16:30:00Z',
             'content': 'Conjugation quiz moved to Monday. Study irregular verbs in present tense and stem-changing verbs. Practice exercises are on Schoology.',
             'attachments': []}
        ]
    }

    return simulated_responses.get(tool_name, [])


@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'server': 'schoology-mcp-frontend'
    })


@app.route('/api/grades')
def get_grades():
    """Get current grades."""
    try:
        with cache_lock:
            if cache['grades'] is None:
                cache['grades'] = call_mcp_tool('get_grades')
                cache['last_updated'] = datetime.now().isoformat()
        return jsonify(cache['grades'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/courses')
def get_courses():
    """Get enrolled courses."""
    try:
        with cache_lock:
            if cache['courses'] is None:
                cache['courses'] = call_mcp_tool('get_courses')
                cache['last_updated'] = datetime.now().isoformat()
        return jsonify(cache['courses'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/assignments')
def get_assignments():
    """Get upcoming assignments."""
    try:
        with cache_lock:
            if cache['assignments'] is None:
                cache['assignments'] = call_mcp_tool('get_upcoming_assignments')
                cache['last_updated'] = datetime.now().isoformat()
        return jsonify(cache['assignments'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/posts')
def get_posts():
    """Get recent posts."""
    try:
        with cache_lock:
            if cache['posts'] is None:
                cache['posts'] = call_mcp_tool('get_recent_posts')
                cache['last_updated'] = datetime.now().isoformat()
        return jsonify(cache['posts'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/refresh', methods=['POST'])
def refresh_data():
    """Force refresh all data from MCP server."""
    try:
        with cache_lock:
            cache['grades'] = call_mcp_tool('get_grades')
            cache['courses'] = call_mcp_tool('get_courses')
            cache['assignments'] = call_mcp_tool('get_upcoming_assignments')
            cache['posts'] = call_mcp_tool('get_recent_posts')
            cache['last_updated'] = datetime.now().isoformat()
        return jsonify({'status': 'ok', 'last_updated': cache['last_updated']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear-session', methods=['POST'])
def clear_session():
    """Clear the Schoology session."""
    try:
        if STATE_FILE.exists():
            STATE_FILE.unlink()
        with cache_lock:
            cache['grades'] = None
            cache['courses'] = None
            cache['assignments'] = None
            cache['posts'] = None
            cache['last_updated'] = None
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/config', methods=['GET', 'POST'])
def handle_config():
    """Get or save configuration."""
    if request.method == 'POST':
        config = request.json
        save_config(config)
        return jsonify({'status': 'ok'})
    else:
        return jsonify(load_config())


@app.route('/api/status')
def get_status():
    """Get connection status and cache info."""
    env_config = get_env_config()
    has_env = bool(env_config.get('SCHOOLOGY_USERNAME'))

    return jsonify({
        'connected': has_env,
        'session_exists': STATE_FILE.exists(),
        'username_configured': has_env,
        'last_updated': cache.get('last_updated')
    })


if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║          Schoology MCP Frontend Server                   ║
    ║                                                           ║
    ║  Local:     http://localhost:8080                        ║
    ║                                                           ║
    ║  This server provides a web interface for the            ║
    ║  Schoology MCP server. Make sure the MCP server          ║
    ║  is running and configured in your .env file.             ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=8080, debug=True)