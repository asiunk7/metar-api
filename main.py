from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "METAR API is running!"

@app.route("/metar")
def get_metar():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify({"error": "Missing ICAO code"}), 400

    try:
        url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json"
        res = requests.get(url, timeout=5)
        data = res.json()

        if isinstance(data, list) and len(data) > 0:
            return jsonify(data[0])  # Return object (not array) ✅
        else:
            return jsonify({"error": "METAR not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
