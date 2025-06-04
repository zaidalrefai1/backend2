from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

STATE_FILE = "game_state.json"

def load_game_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {
        "location": "hub",
        "inventory": [],
        "progress": {}
    }

def save_game_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

@app.route('/api/state', methods=['GET'])
def get_state():
    state = load_game_state()
    return jsonify(state)

@app.route('/api/state', methods=['POST'])
def update_state():
    data = request.json
    save_game_state(data)
    return jsonify({"status": "ok"})

@app.route('/api/start', methods=['POST'])
def reset_state():
    state = {
        "location": "hub",
        "inventory": [],
        "progress": {}
    }
    save_game_state(state)
    return jsonify(state)

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
