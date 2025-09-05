from incident_db import insert_incident
from datetime import datetime
from email_alert import send_alert_email

def classify_severity(indicator):
    if "phishing" in indicator.lower() or "spoof" in indicator.lower():
        return "High"
    elif "Matched IP" in indicator or "unauthorized" in indicator:
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

def log_incident(indicator, source_file, action_taken, severity, timestamp, log_path, zone):
    with open(log_path, 'a', encoding='utf-8') as f:
        f.write(f"\n--- Incident Logged: {timestamp} ---\n")
        f.write(f"Source: {source_file}\n")
        f.write(f"Indicator: {indicator}\n")
        f.write(f"Severity: {severity}\n")
        f.write(f"Zone: {zone}\n")
        f.write(f"Action Taken: {action_taken}\n")
    print(f"✅ Incident logged to file: {indicator} → {severity} | Zone: {zone}")

def process_alerts(source_file, log_path):
    with open(source_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        if line.strip() and not line.startswith("Report generated"):
            indicator = line.strip()
            severity = classify_severity(indicator)
            zone = tag_zone(indicator)
            action = "Simulated block" if "IP" in indicator else "Simulated quarantine"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Log to database
            insert_incident(timestamp, source_file, indicator, severity, action, zone)
            print(f"✅ Incident logged to DB: {indicator} → {severity} | Zone: {zone}")

            # Log to file
            log_incident(indicator, source_file, action, severity, timestamp, log_path, zone)

            # Trigger email alert
            if severity == "High":
                send_alert_email(indicator, severity, timestamp, action)
                print("📬 High-severity alert sent via email.")

if __name__ == "__main__":
    process_alerts("reports/alerts.txt", "reports/incident_log.txt")
    process_alerts("reports/phishing_alerts.txt", "reports/incident_log.txt")
