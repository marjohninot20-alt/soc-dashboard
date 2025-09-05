import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert_email(indicator, severity, timestamp, action):
    sender = "marjohninot20@gmail.com"
    receiver = "marjohninot20@gmail.com"  # or whoever should receive the alert

    subject = f"🚨 SOC Alert: {severity} Threat Detected"
    body = f"""
    A new threat has been detected:

    Indicator: {indicator}
    Severity: {severity}
    Timestamp: {timestamp}
    Action Taken: {action}

    Please review immediately.

    --
    SOC Toolkit Alert System
    This is an automated message.
    """

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("marjohninot20@gmail.com", "clnokqpklbxuuyxv")  # Use app password
            server.sendmail(sender, receiver, msg.as_string())
            print("✅ Alert email sent.")
            print("📬 High-severity alert sent via email.")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")