from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# MCP Tools Definition
@app.route('/tools', methods=['GET'])
def get_tools():
    return jsonify({
        "tools": [
            {
                "name": "read_file",
                "description": "Read file from GitHub repo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file", 
                "description": "Write/create file to GitHub repo",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                        "message": {"type": "string"}
                    },
                    "required": ["path", "content", "message"]
                }
            }
        ]
    })

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "MCP Server Running", "version": "1.0"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
