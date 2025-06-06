from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/metar")
def get_metar():
    icao = request.args.get("icao", "").upper()
    if not icao:
        return jsonify([])

    url = f"https://aviationweather.gov/api/data/metar?ids={icao}&format=json"
    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        # Jika data ditemukan, ambil item pertama saja
        if isinstance(data, list) and len(data) > 0:
            return jsonify(data[0])  # ⬅️ return object tunggal
        else:
            return jsonify({"error": "No data found"})  # bukan []

    except Exception as e:
        return jsonify({"error": str(e)})
