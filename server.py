from flask import Flask, jsonify, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "MCP Server is running",
        "version": "1.0",
        "tools_available": ["read_file", "write_file"]
    }), 200

@app.route('/tools', methods=['GET'])
def get_tools():
    return jsonify({
        "tools": [
            {
                "name": "read_file",
                "description": "Read file from repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path to read"
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write or create file in repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "File path"
                        },
                        "content": {
                            "type": "string",
                            "description": "File content"
                        },
                        "message": {
                            "type": "string",
                            "description": "Commit message"
                        }
                    },
                    "required": ["path", "content", "message"]
                }
            }
        ]
    }), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
