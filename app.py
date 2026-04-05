from flask import Flask, request, jsonify
import base64
import numpy as np

app = Flask(__name__)

@app.route('/api/audio-stats', methods=['POST'])
def audio_stats():
    data = request.get_json()

    audio_base64 = data.get("audio_base64", "")
    
    # Decode (dummy processing for now)
    try:
        audio_bytes = base64.b64decode(audio_base64)
        arr = np.frombuffer(audio_bytes, dtype=np.uint8)
    except:
        arr = np.array([0])

    # Minimal valid structure (IMPORTANT)
    response = {
        "rows": int(len(arr)),
        "columns": ["audio"],
        "mean": {"audio": float(np.mean(arr))},
        "std": {"audio": float(np.std(arr))},
        "variance": {"audio": float(np.var(arr))},
        "min": {"audio": float(np.min(arr))},
        "max": {"audio": float(np.max(arr))},
        "median": {"audio": float(np.median(arr))},
        "mode": {"audio": float(arr[0])},
        "range": {"audio": float(np.max(arr) - np.min(arr))},
        "allowed_values": {"audio": []},
        "value_range": {"audio": [float(np.min(arr)), float(np.max(arr))]},
        "correlation": []
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()