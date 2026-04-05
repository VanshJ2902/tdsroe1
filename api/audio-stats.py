from http.server import BaseHTTPRequestHandler
import json
import base64
import numpy as np

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
            audio_base64 = data.get("audio_base64", "")

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

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())