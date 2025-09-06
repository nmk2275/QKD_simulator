from flask import Flask, jsonify, render_template, request
from qkd_backend.qkd_runner import exp1, exp2, exp3
from qkd_backend.qkd_runner.circuit_simulator import run_circuit_simulator

app = Flask(__name__)

# ---- Serve index.html at root ----
@app.route("/")
def home():
    return render_template("index.html")  # Looks in templates/index.html

# ---- Experiment routes ----
@app.route("/run/exp1", methods=["POST"])
def exp1_route():
    result = exp1.run_exp1()
    return jsonify(result)

@app.route("/run/exp2", methods=["POST"])
def exp2_route():
    result = exp2.run_exp2()
    return jsonify(result)

@app.route("/run/exp3", methods=["POST"])
def exp3_route():
    result = exp3.run_exp3()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)