from flask import Flask, request, jsonify
import requests
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route("/metar", methods=["GET"])
def get_metar():
    icao = request.args.get("icao")
    if not icao:
        return jsonify({"error": "Missing ICAO code"}), 400

    url = f"https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1&stationString={icao}"

    try:
        response = requests.get(url)
        tree = ET.fromstring(response.content)
        metar_el = tree.find(".//METAR/raw_text")

        if metar_el is not None:
            return jsonify({"icao": icao, "metar": metar_el.text})
        else:
            return jsonify({"icao": icao, "metar": None, "note": "No METAR data"}), 204

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
