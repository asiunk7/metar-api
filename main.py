from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("CHECKWX_API_KEY")

@app.route("/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao")
    if not icao:
        return jsonify({"results": [{"metar": "Missing ICAO code"}]}), 400

    url = f"https://api.checkwx.com/metar/{icao}/decoded"
    headers = {
        "X-API-Key": API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            metar_text = data["data"][0].get("raw_text", "No METAR available")
            return jsonify({"results": [{"metar": metar_text}]})
        else:
            return jsonify({"results": [{"metar": "No METAR found"}]})
    except Exception as e:
        return jsonify({"results": [{"metar": f"Error: {str(e)}"}]}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
