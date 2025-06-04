from flask import Flask, json, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import markdown

app = Flask(__name__, static_folder='frontend2', static_url_path='')
CORS(app)

# Game state management
STATE_FILE = "game_state.json"
DEFAULT_STATE = {
    "location": "hub",
    "player": {"x": 100, "y": 100},
    "inventory": []
}

def load_game_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return DEFAULT_STATE

def save_game_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# API Endpoints
@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(load_game_state())

@app.route('/api/state', methods=['POST'])
def update_state():
    new_state = request.json
    save_game_state(new_state)
    return jsonify({"status": "ok"})

@app.route('/api/reset', methods=['POST'])
def reset_state():
    save_game_state(DEFAULT_STATE)
    return jsonify(DEFAULT_STATE)

# Markdown rendering
@app.route('/')
def index():
    return serve_markdown('index')

@app.route('/<path:subpath>')
def serve_markdown(subpath):
    # Handle paths with/without trailing slashes
    subpath = subpath.rstrip('/')
    if not subpath or subpath == 'frontend2':
        subpath = 'index'
    
    md_path = os.path.join('frontend2', f'{subpath}.md')
    
    try:
        with open(md_path, 'r') as f:
            content = f.read()
        
        # Basic HTML wrapper
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{subpath}</title>
    <link rel="stylesheet" href="/frontend2/assets/game/style.css">
</head>
<body>
    {markdown.markdown(content)}
</body>
</html>"""
        
        return render_template_string(html)
    
    except FileNotFoundError:
        return "Page not found", 404

# Static files
@app.route('/frontend2/assets/<path:filename>')
def serve_static(filename):
    return send_from_directory('frontend2/assets', filename)

if __name__ == '__main__':
    app.run(port=4100, debug=True)