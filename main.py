from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao")
    if not icao:
        return jsonify({"error": "Missing ICAO code"}), 400

    # Gunakan endpoint JSON
    url = f"https://aviationweather.gov/api/data/metar?format=json&ids={icao}"

    try:
        response = requests.get(url)
        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            metar_data = data[0]
            raw_text = metar_data.get("raw_text")
            if raw_text:
                return jsonify({"icao": icao, "metar": raw_text})
            else:
                return jsonify({"icao": icao, "metar": None, "note": "raw_text not found"}), 204
        else:
            return jsonify({"error": "No METAR data found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
