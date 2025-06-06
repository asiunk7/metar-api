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
            return jsonify({"results": [{"metar": data[0]["raw_text"]}]})
        else:
            return jsonify({"results": [{"metar": "No raw_text available"}]})
    except Exception as e:
        return jsonify({"results": [{"metar": str(e)}]}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
