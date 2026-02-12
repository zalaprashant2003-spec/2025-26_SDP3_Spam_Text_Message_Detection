import os
import base64
import time
import pickle
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# ================= CONFIG ================= #
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHECK_INTERVAL = 60  # seconds

# ✅ Load email-chat map from JSON file instead of .env
JSON_FILE = BASE_DIR / "email_notify.json"

USER_CHAT_MAP = {}
if JSON_FILE.exists():
    with open(JSON_FILE, "r") as f:
        data = json.load(f)
        for item in data:
            USER_CHAT_MAP[item["email"]] = item["chat_id"]

# ========================================== #

# Load ML model
with open("model_store/nb_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("model_store/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)


def authenticate_gmail(email_address):
    BASE_PATH = Path(__file__).resolve().parent
    TOKEN_DIR = BASE_PATH / "tokens"
    TOKEN_DIR.mkdir(exist_ok=True)

    token_file = TOKEN_DIR / f"token_{email_address.replace('@', '_')}.json"
    creds = None

    if token_file.exists():
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                BASE_PATH / "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        token_file.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)



def get_unread_emails(service):
    query = "is:unread newer_than:1d"
    results = service.users().messages().list(
        userId="me", labelIds=["INBOX"], q=query
    ).execute()
    return results.get("messages", [])


def read_email(service, msg_id):
    message = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    subject = ""
    to_email = ""
    for header in headers:
        if header["name"] == "Subject":
            subject = header["value"]
        if header["name"] == "To":
            to_email = header["value"]

    body = ""
    parts = payload.get("parts")
    if parts:
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part["body"].get("data")
                if data:
                    body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
    else:
        data = payload.get("body", {}).get("data")
        if data:
            body = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return subject, to_email, body


def is_spam(text):
    vector = vectorizer.transform([text])
    prediction = model.predict(vector)
    return prediction[0] == 1


def send_telegram_notification(message, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        requests.post(url, data=data, verify=False).raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Telegram error:", e)


def main():
    services = {}

    # Authenticate all accounts ONCE
    for email_address in USER_CHAT_MAP:
        print(f"🔐 Authenticating {email_address}")
        services[email_address] = authenticate_gmail(email_address)

    print("🚀 Gmail spam notifier running")

    while True:
        try:
            for email_address, service in services.items():
                chat_id = USER_CHAT_MAP[email_address]
                messages = get_unread_emails(service)

                for msg in messages:
                    subject, to_email, email_text = read_email(service, msg["id"])

                    print("=" * 50)
                    print(f"Account: {email_address}")
                    print(f"To: {to_email}")
                    print(f"Subject: {subject}")
                    print("=" * 50)

                    if not is_spam(email_text):
                        send_telegram_notification(
                            f"📩 New email for {email_address}\nSubject: {subject}",
                            chat_id
                        )

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("🛑 Stopped by user")
            break

        except Exception as e:
            print("⚠ Error:", e)
            time.sleep(10)

if __name__ == "__main__":
    main()
