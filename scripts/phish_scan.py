from datetime import datetime

def scan_email_headers(file_path):
    with open(file_path, 'r') as f:
        headers = f.read()

    findings = []

    # Check for mismatched From and Reply-To
    if "Reply-To:" in headers and "From:" in headers:
        from_line = [line for line in headers.splitlines() if line.startswith("From:")][0]
        reply_line = [line for line in headers.splitlines() if line.startswith("Reply-To:")][0]
        if from_line != reply_line:
            findings.append("⚠️ Mismatched From and Reply-To addresses")

    # Check for suspicious keywords
    suspicious_keywords = ["urgent", "verify", "reset", "click here", "confirm"]
    for keyword in suspicious_keywords:
        if keyword.lower() in headers.lower():
            findings.append(f"⚠️ Suspicious keyword detected: '{keyword}'")

    # Check for unknown sender domain
    if "Received:" in headers and "evil-domain.com" in headers:
        findings.append("⚠️ Email received from suspicious domain: evil-domain.com")

    return findings

from milestone_tracker import update_milestones
update_milestones("phishing_detections")

from datetime import datetime

def save_phish_report(findings, report_path):
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"Phishing Scan Report: {datetime.now()}\n")
        for item in findings:
            f.write(f"{item}\n")
    print(f"✅ Report saved to {report_path}")

if __name__ == "__main__":
    results = scan_email_headers("emails/sample_email.txt")
    if results:
        print("Phishing Indicators Found:")
        for r in results:
            print(r)
        print("📥 Simulated Action: Email moved to quarantine.")
        print("📧 Simulated Action: Alert sent to user.")
        save_phish_report(results, "reports/phishing_alerts.txt")
    else:
        print("✅ No phishing indicators detected.")
