import os
import base64
import time
import pickle
import requests
import certifi

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# ================= CONFIG ================= #
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CHECK_INTERVAL = 60  # seconds
# ========================================== #

# Load ML model
with open("model_store/nb_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_store/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def authenticate_gmail():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_unread_emails(service):
    # Gmail search query: unread emails from last 1 day
    query = "is:unread newer_than:1d"  # 1 day = 24 hours
    results = service.users().messages().list(
        userId="me", labelIds=["INBOX"], q=query
    ).execute()

    return results.get("messages", [])



def read_email(service, msg_id):
    message = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    payload = message["payload"]
    headers = payload.get("headers", [])

    subject = ""
    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]

    body = ""
    parts = payload.get("parts")
    if parts:
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    else:
        data = payload["body"].get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return subject + " " + body


def is_spam(text):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)
    return prediction[0] == 1


def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        # Use certifi to verify SSL safely
        response = requests.post(url, data=data, verify=False)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Telegram error:", e)


def main():
    service = authenticate_gmail()
    print("📧 Gmail Spam Notifier Started...")

    processed_ids = set()

    while True:
        try:
            messages = get_unread_emails(service)

            for msg in messages:
                msg_id = msg["id"]
                if msg_id in processed_ids:
                    continue

                email_text = read_email(service, msg_id)

                if not is_spam(email_text):
                    send_telegram_notification(
                        "✅ New email received (not spam)."
                    )
                else:
                    send_telegram_notification(
                        "🚫 Spam email detected. Notification suppressed."
                    )


                processed_ids.add(msg_id)

            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print("Error:", e)
            time.sleep(10)


if __name__ == "__main__":
    main() 