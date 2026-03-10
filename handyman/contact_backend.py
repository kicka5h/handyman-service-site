"""
Contact form backend — SQLite storage + Gmail SMTP notification.

All free, no external services required.

Setup:
  Copy .env.example to .env and fill in your values.
  Gmail requires an App Password (not your regular password):
    Google Account → Security → 2-Step Verification → App Passwords
"""
import os
import smtplib
import sqlite3
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# On Fly.io, DB_PATH is set to /data/submissions.db via fly.toml [env].
# Locally it defaults to submissions.db in the project root.
_default_db = Path(__file__).parent.parent / "submissions.db"
_configured = Path(os.getenv("DB_PATH", str(_default_db)))
# Fall back to /tmp if the configured directory doesn't exist (e.g. volume not mounted)
DB_PATH = _configured if _configured.parent.exists() else Path("/tmp/submissions.db")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", SMTP_USER)


# ── Database ──────────────────────────────────────────────────────────────────

def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT NOT NULL,
                email        TEXT NOT NULL,
                phone        TEXT,
                message      TEXT NOT NULL,
                submitted_at TEXT NOT NULL
            )
        """)
        conn.commit()


def save_submission(name: str, email: str, phone: str, message: str) -> None:
    submitted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO submissions (name, email, phone, message, submitted_at) VALUES (?, ?, ?, ?, ?)",
            (name, email, phone or "", message, submitted_at),
        )
        conn.commit()
    print(f"[DB] Saved submission from {name} <{email}>")


# ── Email ─────────────────────────────────────────────────────────────────────

def send_notification(name: str, email: str, phone: str, message: str) -> None:
    if not SMTP_USER or not SMTP_PASSWORD:
        print("[Email] SMTP not configured — skipping notification. Set SMTP_USER and SMTP_PASSWORD in .env")
        return

    submitted_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"New Quote Request from {name}"
    msg["From"] = SMTP_USER
    msg["To"] = NOTIFY_EMAIL
    msg["Reply-To"] = email

    plain = f"""\
New quote request via ProHandyman website:

  Name:    {name}
  Email:   {email}
  Phone:   {phone or "Not provided"}
  Message: {message}

  Submitted: {submitted_at}

Reply directly to this email to reach {name}.
"""

    html = f"""\
<html><body style="font-family:sans-serif;color:#1E293B;max-width:600px;margin:0 auto">
  <div style="background:#0B3D2E;padding:24px 32px;border-radius:8px 8px 0 0">
    <h2 style="color:white;margin:0">New Quote Request</h2>
    <p style="color:rgba(255,255,255,0.7);margin:4px 0 0">ProHandyman Website</p>
  </div>
  <div style="background:#F2FDF7;padding:24px 32px;border:1px solid #D1FAE5;border-top:none">
    <table style="width:100%;border-collapse:collapse">
      <tr><td style="padding:8px 0;color:#64748B;width:90px">Name</td>
          <td style="padding:8px 0;font-weight:600">{name}</td></tr>
      <tr><td style="padding:8px 0;color:#64748B">Email</td>
          <td style="padding:8px 0"><a href="mailto:{email}" style="color:#D97706">{email}</a></td></tr>
      <tr><td style="padding:8px 0;color:#64748B">Phone</td>
          <td style="padding:8px 0">{phone or "Not provided"}</td></tr>
    </table>
    <hr style="border:none;border-top:1px solid #D1FAE5;margin:16px 0">
    <p style="color:#64748B;margin:0 0 6px;font-size:0.88rem">MESSAGE</p>
    <p style="margin:0;line-height:1.6;white-space:pre-wrap">{message}</p>
  </div>
  <div style="background:#F8FAFC;padding:12px 32px;border:1px solid #E2E8F0;border-top:none;
              border-radius:0 0 8px 8px;font-size:0.82rem;color:#94A3B8">
    Submitted {submitted_at} · Reply to this email to contact {name} directly.
  </div>
</body></html>
"""

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, NOTIFY_EMAIL, msg.as_string())
        print(f"[Email] Notification sent to {NOTIFY_EMAIL}")
    except Exception as exc:
        print(f"[Email] Failed to send notification: {exc}")


# ── Combined handler (call this from state + API) ─────────────────────────────

def handle_submission(name: str, email: str, phone: str, message: str) -> None:
    try:
        save_submission(name, email, phone, message)
    except Exception as exc:
        print(f"[DB] Failed to save submission: {exc}")
    send_notification(name, email, phone, message)
