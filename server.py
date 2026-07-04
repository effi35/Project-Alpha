#!/usr/bin/env python3
import os
import sys
import json
from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# Simple request logger
@app.before_request
def log_request():
    print(f"[REQUEST] {request.method} {request.path}", file=sys.stderr)

# Error handler
@app.errorhandler(Exception)
def handle_error(error):
    print(f"[ERROR] {str(error)}", file=sys.stderr)
    return jsonify({"error": str(error)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "name": "GitHub Project-Alpha MCP",
        "version": "1.0.0",
        "status": "running"
    }), 200

# MCP Tools discovery endpoint
@app.route('/tools', methods=['GET', 'POST'])
def list_tools():
    tools = {
        "tools": [
            {
                "name": "read_file",
                "description": "Read file from GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to file in repository"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write or create file in GitHub repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path in repository"
                        },
                        "content": {
                            "type": "string",
                            "description": "File content to write"
                        },
                        "message": {
                            "type": "string",
                            "description": "Git commit message"
                        }
                    },
                    "required": ["path", "content", "message"]
                }
            },
            {
                "name": "list_files",
                "description": "List files in repository directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Directory path (optional, defaults to root)"
                        }
                    }
                }
            }
        ]
    }
    return jsonify(tools), 200

# Tool execution endpoint
@app.route('/call_tool', methods=['POST'])
def call_tool():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No JSON data"}), 400
    
    tool_name = data.get('name')
    tool_input = data.get('input', {})
    
    # Placeholder responses for MCP compatibility
    if tool_name == "read_file":
        return jsonify({
            "content": f"File: {tool_input.get('path', 'unknown')}"
        }), 200
    elif tool_name == "write_file":
        return jsonify({
            "success": True,
            "message": f"File {tool_input.get('path')} written"
        }), 200
    elif tool_name == "list_files":
        return jsonify({
            "files": ["placeholder.txt"]
        }), 200
    else:
        return jsonify({"error": f"Unknown tool: {tool_name}"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[START] Starting MCP Server on port {port}", file=sys.stderr)
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )
