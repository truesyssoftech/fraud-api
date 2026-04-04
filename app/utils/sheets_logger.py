import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
import json

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

        creds_dict = json.loads('{"type":"service_account","project_id":"automation-468806","private_key_id":"7f3634490ac2414d5d1268b47e4a96f6c50e85f2","private_key":"-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDHcBq3w89Kas6C\nBOcJxO04OTC/XSqscf1wkfpDtN/7vRJnDa7f2j0ssre30SUF9zDdEjSDmsHXKzgm\nVM4IiQwtlEipxknlrJm+t97NhqJDiATHyILIR7A8NDzPyf1IQNpAKsim00JWCG9b\nBM1uKfAITtpdXTjvkg/YSTfoybtP21I3Y1jkFdm7GpsDsmgV4vy8SGTHRqYoYPGk\nedkch14HlbD+hP0Xixdn8rcik7JG1LxGZ3hvoqhuLEdLtkqY2qXrY8N0/hU2wF5N\nwejAhqJJsR0hBcm7kx6Y7kHLCD/EVPlwg05kaBg7G0dfD67Cm4MiIOMwfDhs81Du\nVCKa7kA5AgMBAAECggEAAzy01lBBlFfk97PMKzqszgmRmr2QpIFqJ3JbIU+1hgDE\n5HLSqJQCg6/37u4gX3cqbiAuRYeUx2EOdYLRYE6XKcM7JbRP/UAes7uIzIW3qwhx\naWu+AbG2MNf5N7cz2wEgecOoA5swu7RB2HScwAHCwWPERBkwBCV3B9/yXh8uIObr\nVq4yenwTsyrlTqvY7UeCLWUPj9v0O0Eu14mcwe6jeRoSNUlJcZCVLkYLi//+o+Du\n3rxp70XHcuGH+rgR0rok87tjzw7PoywBxi+bZUL/IWV7fPyIS+1EQ16axr6jXUKk\nd1bkmFvxH2wxKQAe66Y4Mvwx9TgV6bzjuYGMhYsInQKBgQDwGooblZfRPIsbv6l1\neeQo6x/5y/s4f9z7usfWIPLQMIMp26VqXqnSmrXPqDHRijPLco0o2mOrIYH7cHH+\nqPPRSrpnUF0VArtNGBpxlg0SBga6Yo5joPRpfWVjEhvkJgyThs9ejQ7O4h6V3zlW\nZaThXq/K3kMMa6CTqF/O8vGutQKBgQDUpFSZQR9ZmPMit3QTusFKH6zpGw7Cvadf\nzzvl2jbHx+Z5F5BH+TCBqaBW1OuAJKKvkYsX4s6Mgz1AbNplnbmLMkw3J4xRP7eW\nm6lfAumdpYas/pjIPftBQhJe+B3Y2FcGE0ATZd6djOS6W32Ptawf4RFyd+A3igEa\n6hPYqGT59QKBgAPnyptMQZ3rqC+ZXH5Gr0ljGbAMe1ed7NBDZ4C6JHjycQ+7POOQ\nCp8cWRy5laXc457JjDY/5yMfdmfKmnAT+3NKDeIkUn9G/hjw7W0vjaLfajiZ5csF\nETSuD3ofD0kUvVug87qL/NOspea2LM6U9KudyKo6F0kabxA3yuco2HmJAoGAIw4E\nNE+cD3U7f9mmdSowezvFkZg4UrpZQV40javvo/e8cvIDgxn9eSKxoB7xw+pGN5NS\nztlBG8D29Av95Qqfb+cW0XDfnPVYGqgGv/cG9Eo5bYN7RGeTaCqwRJ+6q+jeT84U\nnh4JGQgFHQPAK1TTz12XNru0ZvOFQx6brvfzzZECgYBCk7oZo2ffONuTV9E0EWQw\n7/KnWh5afc+FOchy1qgkEJqcqnO4F0HQ+Cpx/s8guf/5J5EgBJDT2UJMSo598tFr\nm+oUSAl1izso/giHgSMRAEoeSjsEgHl8sqkKOX/AbZPsAkqizqUf1YhQEK+H5z7c\nM48Q56b0MGDscIrgeTfvOQ==\n-----END PRIVATE KEY-----\n","client_email":"spam-detaction-db@automation-468806.iam.gserviceaccount.com","client_id":"102525807110667019128","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url":"https://www.googleapis.com/robot/v1/metadata/x509/spam-detaction-db%40automation-468806.iam.gserviceaccount.com","universe_domain":"googleapis.com"}')

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

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