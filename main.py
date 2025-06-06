from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao")
    if not icao:
        return jsonify({"error": "Missing ICAO code"}), 400

    url = f"https://tgftp.nws.noaa.gov/data/observations/metar/stations/{icao.upper()}.TXT"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            lines = response.text.strip().split("\n")
            if len(lines) >= 2:
                return jsonify({"metar": lines[1]})
            else:
                return jsonify({"metar": None})
        else:
            return jsonify({"metar": None}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
