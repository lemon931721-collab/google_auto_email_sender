# Auto Sending Email

A small Python script that sends email through the **Gmail API** over HTTPS (port 443).

It uses the Gmail API instead of SMTP because outbound SMTP ports (465/587) are blocked on some networks, firewalls, and hosting providers. If HTTPS works, this works.

## Features

- Sends plain text email from your Gmail account
- OAuth login once via the browser, then reuses a saved token
- Credentials and addresses are loaded from a `.env` file
- No App Password needed

## Project structure

```
5.autoSendingEmail/
├── sendemail.py        # main script
├── .env                # your addresses (not committed)
├── credentials.json    # Google OAuth client file (not committed)
├── token.json          # created on first run (not committed)
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- **64-bit Python 3.10+** (32-bit Python can fail to install the `cryptography` dependency)
- A Google account (Gmail)
- Outbound HTTPS access to `gmail.googleapis.com`

Check your Python build:

```powershell
python -c "import struct; print(struct.calcsize('P')*8)"
```

It should print `64`.

## Setup

### 1. Create a virtual environment and install dependencies

```powershell
py -3.14-64 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Use the version you have installed (for example `py -3.13-64`). `py -0p` lists installed Pythons.

`requirements.txt`:

```
google-api-python-client
google-auth-oauthlib
google-auth-httplib2
python-dotenv
```

### 2. Set up the Google Cloud project

1. Go to <https://console.cloud.google.com> and create or select a project.
2. Open **APIs & Services → Library**, search for **Gmail API**, and click **Enable**.
3. Open **Google Auth Platform** and click **Get started**:
   - **App Information:** enter an app name and your support email
   - **Audience:** choose **External**
   - **Contact Information:** enter your email
   - Agree to the policy and click **Create**
4. Open **Audience → Test users → + Add users**, add your Gmail address, and save.
5. Open **Clients → + Create client**, choose **Desktop app**, and click **Create**.
6. Click **Download JSON** and save it as `credentials.json` in the project folder.

### 3. Create the `.env` file

In the project folder, create `.env`:

```
GMAIL_ADDRESS=your_email@gmail.com
RECEIVER_EMAIL=receiver@example.com
```

Do not wrap values in quotes. `GMAIL_ADDRESS` must be the account you sign in with in the browser.

## Usage

```powershell
py .\sendemail.py
```

On the first run a browser window opens:

1. Sign in with your Gmail account.
2. If you see "Google hasn't verified this app", click **Advanced → Go to (app name)**. This is normal for your own personal app.
3. Allow the requested access (send email only).

A `token.json` file is saved, and later runs send without any login. On success you'll see:

```
Email sent successfully! Message ID: ...
```

### Sending a different message

`sendemail.py` exposes a `send_email(to, subject, body)` function. Edit the last lines of the script, or import it from another script:

```python
from sendemail import send_email

send_email("someone@example.com", "Subject here", "Message body here")
```

## Troubleshooting

| Problem | Cause and fix |
|---|---|
| `TimeoutError` / `WinError 10060` with SMTP | SMTP ports are blocked on your network. This project avoids SMTP by using the Gmail API. |
| `pip install` fails building `cryptography` (`link.exe not found`) | You are on 32-bit Python. Install 64-bit Python and recreate `.venv`. |
| `Missing credentials.json` | Download the OAuth client JSON (Desktop app) from Google Cloud and save it in the project folder. |
| `access_denied` / "app not verified" | Add your Gmail address under **Audience → Test users**. |
| `Gmail API has not been used in project` | Enable the Gmail API under **APIs & Services → Library**. |
| Login stops working after about 7 days | While the OAuth app is in **Testing** mode, tokens expire after about a week. Delete `token.json` and run again, or click **Publish app** on the consent screen. |
| `invalid_grant` | Delete `token.json` and sign in again. |
| Running on a server with no browser | Run the script once on a normal PC, then copy `token.json` to the server. |
| `py .\sendemail.py\` says invalid argument | Remove the trailing `\`. Use `py .\sendemail.py`. |

## Security

- Never commit `.env`, `credentials.json`, or `token.json`. Anyone with `token.json` can send email as you.
- If a secret is ever exposed (pasted in a chat, committed to Git), revoke it and create a new one. Old Gmail App Passwords can be removed at <https://myaccount.google.com/apppasswords>.
- The script requests only the `gmail.send` scope, so it can send email but cannot read your inbox.

`.gitignore`:

```
.venv/
.env
credentials.json
token.json
__pycache__/
```

## How it works

1. `python-dotenv` loads `GMAIL_ADDRESS` and `RECEIVER_EMAIL` from `.env`.
2. `get_service()` loads `token.json`, refreshes it if expired, or starts the browser login using `credentials.json`.
3. `send_email()` builds an `EmailMessage`, base64url-encodes it, and calls `users().messages().send()` on the Gmail API.

## License

Personal project. Add a license here if you plan to share it.
yolo
