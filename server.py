from flask import Flask, request, jsonify
from flask_cors import CORS
from model.wrapper import GameModel


app = Flask(__name__)
CORS(app)

# Store model globally for simplicity
game_model = None

@app.route("/init", methods=["POST"])
def init_model():
    global game_model
    data = request.get_json()
    game_model = GameModel(data)
    return jsonify({ "grid_state": game_model.state, "status": "initialized" })

@app.route("/step", methods=["POST"])
def step_model():
    global game_model
    if not game_model:
        return jsonify({ "grid_state": None, "status": "error", "error": "Model not initialized" }), 400
    new_state = game_model.step()
    return jsonify({ "grid_state": new_state, "status": "running" })

if __name__ == "__main__":
    app.run(debug=True)
