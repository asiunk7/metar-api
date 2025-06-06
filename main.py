from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/metar")
def get_all_indonesia_metar():
    prefixes = ["WI", "WA", "WB", "WR"]
    station_url = "https://aviationweather.gov/docs/metar/stations.txt"
    headers = {"User-Agent": "Mozilla/5.0"}

    station_data = requests.get(station_url, headers=headers).text
    icao_codes = []

    for line in station_data.splitlines():
        if line.startswith(tuple(prefixes)):
            icao = line[:4]
            icao_codes.append(icao)

    icao_str = ",".join(icao_codes)
    metar_url = f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao_str}&format=raw&hours=1"
    raw_text = requests.get(metar_url, headers=headers).text.strip()

    result = []
    for line in raw_text.splitlines():
        parts = line.split()
        if parts:
            icao = parts[0]
            result.append({"icao": icao, "metar": line})

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
