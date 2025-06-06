from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao")
    if not icao:
        return jsonify({"error": "Missing ICAO code"}), 400

    url = f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao}&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            return jsonify({"metar": data[0].get("raw_text", "No raw_text available")})
        else:
            return jsonify({"error": "No METAR found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
