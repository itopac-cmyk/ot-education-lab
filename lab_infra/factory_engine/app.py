from flask import Flask, render_template, jsonify, request
import time
app = Flask(__name__)
state = {
    "pump": {"speed": 50, "temperature": 45.0, "status": "OPERATIONAL"},
    "robot": {"mode": "AUTO", "collision_risk": 0.0, "offset_x": 0.0},
    "compliance": {"mvo_1_1_9": True, "cra_integrity": True}
}
@app.route('/')
def index(): return render_template('twin.html')
@app.route('/api/state')
def get_state():
    if state["pump"]["speed"] > 100:
        state["pump"]["temperature"] += 0.5
        state["compliance"]["mvo_1_1_9"] = False
    return jsonify(state)
@app.route('/api/update', methods=['POST'])
def update_state():
    data = request.json
    if "pump_speed" in data: state["pump"]["speed"] = data["pump_speed"]
    if "vision_offset" in data:
        state["robot"]["offset_x"] = data["vision_offset"]
        if abs(data["vision_offset"]) > 5.0: state["compliance"]["cra_integrity"] = False
    return jsonify({"status": "synced"})
if __name__ == '__main__': app.run(host='0.0.0.0', port=9000)
