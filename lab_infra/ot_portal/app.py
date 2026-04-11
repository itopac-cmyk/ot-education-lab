from flask import Flask, render_template
app = Flask(__name__)
SCENARIOS = [{"id": 1, "name": "Modbus Manipulation", "description": "Sabotage PLC registers.", "url": "http://localhost:8080", "tech": "Modbus TCP"}]
@app.route('/')
def index(): return render_template('index.html', scenarios=SCENARIOS)
if __name__ == '__main__': app.run(host='0.0.0.0', port=9000)
