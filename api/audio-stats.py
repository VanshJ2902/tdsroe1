import json
import base64
import numpy as np

def handler(request):
    try:
        if request.method != "POST":
            return {
                "statusCode": 405,
                "body": json.dumps({"error": "Method not allowed"})
            }

        body = json.loads(request.body)
        audio_base64 = body.get("audio_base64", "")

        audio_bytes = base64.b64decode(audio_base64)
        arr = np.frombuffer(audio_bytes, dtype=np.uint8)

        if len(arr) == 0:
            arr = np.array([0])

    except:
        arr = np.array([0])

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

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response)
    }