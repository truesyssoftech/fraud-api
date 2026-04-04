import requests
import threading
from datetime import datetime
import os

LOGGER_API_URL = os.getenv("LOGGER_API_URL")


def log_to_sheets(message, final_label, confidence):
    if not LOGGER_API_URL:
        print("⚠️ LOGGER_API_URL not set")
        return

    def call_api():
        try:
            payload = {
                "timestamp": datetime.now().isoformat(),
                "message": message,
                "final_label": final_label,
                "confidence": confidence
            }

            requests.post(
                LOGGER_API_URL,
                json=payload,
                timeout=2
            )

        except Exception as e:
            print("❌ Sheets API error:", e)

    threading.Thread(target=call_api).start()