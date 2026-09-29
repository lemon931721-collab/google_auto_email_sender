import base64
import os
from email.message import EmailMessage
from pathlib import Path
import time
import random

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

SENDER_EMAIL = os.getenv("GMAIL_ADDRESS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
DELAY = int(os.getenv("DELAY"))
TITLE = "A Potential Opportunity to Work Together"
CONTENT = """
Hi.

I hope you’re doing well. I hope you don’t mind me reaching out. I came across your profile and thought you might be someone I could potentially work with.

My name is  Jonathan, and I’m a software developer based in Singapore. I’ve been working remotely with clients for around eight years.

I’m reaching out because I have a business idea that I’d like to share with you. It’s a little different from a typical opportunity, and you wouldn’t need any programming or technical experience.

The basic idea is to explore whether we could work together on legitimate software-related opportunities where this type of collaboration is appropriate and permitted. I would handle the technical development, and we would clearly agree on any responsibilities on your side before moving forward.

There may be a financial benefit for you as well, but I’d rather explain the details clearly instead of making the email too long.

I realize this message is unexpected since we haven’t spoken before, so there’s absolutely no pressure. If you’re curious, simply reply to this email and I’ll be happy to explain the idea and answer any questions you have.

If you’d prefer to speak by phone, you can also reach me here:

WhatsApp: +12273106831
Phone: +14056430940
Telegram:  @elkeins

If it’s not something you’re interested in, no worries at all. I appreciate you taking the time to read my message.

Best regards,
Jonathan
"""

if not SENDER_EMAIL or not RECEIVER_EMAIL:
    raise SystemExit("Set GMAIL_ADDRESS and RECEIVER_EMAIL in your .env file")

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


def get_service():
    """Log in once via the browser, then reuse token.json on later runs."""
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None  # refresh token expired or revoked, log in again
        if not creds or not creds.valid:
            if not CREDENTIALS_FILE.exists():
                raise SystemExit(f"Missing {CREDENTIALS_FILE.name}. Download it from Google Cloud Console.")
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email(to, subject, body):
    msg = EmailMessage()
    msg["To"] = to
    msg["From"] = SENDER_EMAIL
    msg["Subject"] = subject
    msg.set_content(body)

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    try:
        service = get_service()
        result = service.users().messages().send(userId="me", body={"raw": raw}).execute()
        print(f"Email sent successfully! Message ID: {result['id']}")
    except HttpError as e:
        print(f"Gmail API error: {e}")

lines_list = []

if __name__ == "__main__":
    try:
        with open('gmail_list.txt', 'r', encoding='utf-8') as file:
            lines_list = [line.strip() for line in file if line.strip()]
        for i in range(400):
            chosen = random.choice(lines_list)
            send_email(chosen, TITLE, CONTENT)
            time.sleep(DELAY)
    except FileNotFoundError:
        print("Error: File not found.")
    except KeyboardInterrupt:
        print("\nStopped by user.")
