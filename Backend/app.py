from flask import Flask, request, jsonify
from flask_cors import CORS
from Check_Scheme import match_schemes

app = Flask(__name__)
CORS(app)  # Allows frontend to talk to this server

# ── HEALTH CHECK ──
# Visit http://localhost:5000/ to confirm server is running
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Sahaj backend is running!"})


# ── MAIN MATCHING ENDPOINT ──
# Frontend sends answers here, we return matching schemes
@app.route("/match", methods=["POST"])
def match():
    data = request.json

    # Validate that all 4 answers are present
    required = ["gender","age", "income", "location", "occupation"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    # Run matching logic
    matched = match_schemes(
        gender=data["gender"], 
        age=data["age"],
        income=data["income"],
        location=data["location"],
        occupation=data["occupation"]
    )

    return jsonify({
        "count": len(matched),
        "schemes": matched
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)