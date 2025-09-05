import imaplib
import email
from email.header import decode_header
from datetime import datetime
from incident_db import insert_incident
from email_alert import send_alert_email

from dotenv import load_dotenv
import os

load_dotenv()
username = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PASS")

def classify_severity(indicator):
    if "phishing" in indicator.lower() or "spoof" in indicator.lower():
        return "High"
    elif "unauthorized" in indicator.lower() or "Matched IP" in indicator:
        return "Medium"
    else:
        return "Low"

def tag_zone(indicator):
    indicator = indicator.lower()
    if "phishing" in indicator or "spoof" in indicator:
        return "Dark Forest"
    elif "ip" in indicator or "unauthorized" in indicator:
        return "Firewall Citadel"
    elif "reply-to" in indicator or "mismatch" in indicator:
        return "Echo Chamber"
    elif "file" in indicator or "exfil" in indicator:
        return "Data Vault"
    elif "missing log" in indicator or "telemetry" in indicator:
        return "Signal Abyss"
    else:
        return "FreeWorld Outlands"

def clean_text(text):
    if isinstance(text, bytes):
        return text.decode("utf-8", errors="ignore")
    return text

def scan_inbox():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")

    # Add session header to log file
    with open("reports/email_scan_log.txt", 'a', encoding='utf-8') as log:
        log.write("\n--- Email Scan Session: {} ---\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    # Limit scan to first 50 unread emails
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()[:50]

    for eid in email_ids:
        res, msg_data = mail.fetch(eid, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        subject = clean_text(subject)
        sender = clean_text(msg.get("From"))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        indicator = f"Subject: {subject} | From: {sender}"
        severity = classify_severity(indicator)
        zone = tag_zone(indicator)
        action = "Flagged for review"

        insert_incident(timestamp, "Gmail Inbox", indicator, severity, action, zone)
        print(f"✅ Email scanned: {indicator} → {severity} | Zone: {zone}")

        # Log to file
        with open("reports/email_scan_log.txt", 'a', encoding='utf-8') as log:
            log.write(f"{timestamp} | {indicator} | {severity} | Zone: {zone}\n")

        # Send alert if high severity
        if severity == "High":
            send_alert_email(indicator, severity, timestamp, action)

        # Mark email as read
        mail.store(eid, '+FLAGS', '\\Seen')

    mail.logout()

if __name__ == "__main__":
    scan_inbox()
