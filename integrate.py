#!/usr/bin/env python3
"""
Integration script that shows how to connect the frontend to the actual
Schoology MCP server. This demonstrates the MCP protocol communication.
"""

import subprocess
import json
import sys

def call_mcp(tool_name, arguments=None):
    """
    Call the MCP server using claude mcp command.
    This requires the schoology MCP server to be registered.
    """
    cmd = [
        'claude', 'mcp', 'call', 'schoology',
        '--tool', tool_name
    ]

    if arguments:
        import argparse
        for key, value in arguments.items():
            cmd.extend([f'--{key}', str(value)])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"MCP call failed: {result.stderr}")

    return json.loads(result.stdout)


def main():
    """Demonstrate MCP tool calls."""
    print("Schoology MCP Integration Demo")
    print("=" * 40)

    tools = [
        ('get_grades', {}),
        ('get_courses', {}),
        ('get_upcoming_assignments', {}),
        ('get_recent_posts', {})
    ]

    for tool_name, args in tools:
        try:
            print(f"\nCalling {tool_name}...")
            result = call_mcp(tool_name, args)
            print(f"Success: {len(result)} items returned")
            if result:
                print(f"  First item: {json.dumps(result[0], indent=2)[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
            print("  Make sure the Schoology MCP server is registered:")
            print("  claude mcp add schoology -- /path/to/.venv/bin/python /path/to/server.py")

    print("\n" + "=" * 40)
    print("For the web frontend, run: python server.py")


if __name__ == '__main__':
    main()