import re

def detect_suspicious_ips(log_path):
    with open(log_path, 'r') as file:
        logs = file.readlines()

    suspicious = []
    for line in logs:
        if "Failed login" in line or "unauthorized" in line:
            ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_match:
                suspicious.append(ip_match.group())

    return set(suspicious)

from milestone_tracker import update_milestones
update_milestones("ip_detections")

from datetime import datetime

def save_to_report(matches, report_path):
    with open(report_path, 'w') as f:
        f.write(f"Report generated: {datetime.now()}\n")
        f.write("Suspicious IPs Detected:\n")
        for match in matches:
            f.write(f"{match}\n")
    print(f"✅ Report saved to {report_path}")

if __name__ == "__main__":
    results = detect_suspicious_ips("logs/sample.log")
    for ip in results:
        print(f"⚠️ {ip}")
        print(f"🛡️ Simulated Action: Blocking IP {ip}")
    save_to_report(results, "reports/alerts.txt")
