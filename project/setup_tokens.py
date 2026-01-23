import os
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

ACCOUNTS = [
    "atikvahora26@gmail.com",
    "23ceuoz156@ddu.ac.in",
    # add more users here
]

os.makedirs("tokens", exist_ok=True)

for email in ACCOUNTS:
    token_path = f"tokens/token_{email.replace('@','_')}.json"

    if os.path.exists(token_path):
        print(f"✅ Token already exists for {email}")
        continue

    print(f"\n🔐 Login required for: {email}")
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)

    with open(token_path, "w") as f:
        f.write(creds.to_json())

    print(f"✅ Token saved → {token_path}")
