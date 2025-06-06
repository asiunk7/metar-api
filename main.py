from flask import Flask, request, jsonify
import requests

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
            return jsonify({"metar": data[0]["raw_text"]})
        else:
            return jsonify({"metar": "No METAR found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
