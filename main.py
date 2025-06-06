from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route("/metar")
def get_metar_indonesia():
    icao_list = [
        "WIII", "WADD", "WAJJ", "WAAA", "WIMM", "WIBB",
        "WICK", "WIOO", "WAMM", "WABL", "WAMT", "WAMW", "WAMK", "WAMR",
        "WAON", "WAOO", "WARA", "WARS", "WASF", "WASS", "WBSB", "WBGG"
    ]
    icao_str = ",".join(icao_list)
    metar_url = f"https://aviationweather.gov/cgi-bin/data/metar.php?ids={icao_str}&format=raw&hours=1"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        raw_data = requests.get(metar_url, headers=headers, timeout=10).text.strip()
        result = []
        for line in raw_data.splitlines():
            parts = line.split()
            if parts:
                icao = parts[0]
                result.append({"icao": icao, "metar": line})
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
