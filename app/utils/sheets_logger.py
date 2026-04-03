import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

SHEET_NAME = "Fraud Logs"

client = None
sheet = None


def init_sheets():
    global client, sheet

    if client is not None:
        return

    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(
            "service_account.json", scope
        )

        client = gspread.authorize(creds)
        sheet = client.open(SHEET_NAME).sheet1

        print("✅ Google Sheets connected")

    except Exception as e:
        print("❌ Sheets init failed:", e)


def log_to_sheets(message, final_label, confidence):
    try:
        init_sheets()

        if sheet is None:
            return

        sheet.append_row([
            datetime.now().isoformat(),
            message,
            final_label,
            confidence
        ])

    except Exception as e:
        print("❌ Sheets logging error:", e)