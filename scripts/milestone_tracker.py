import json
from datetime import datetime

def update_milestones(detection_type):
    path = "reports/milestones.json"
    with open(path, 'r') as f:
        data = json.load(f)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data["total_detections"] += 1
    data[detection_type] += 1

    if not data["first_detection"]:
        data["first_detection"] = now
    data["last_detection"] = now

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"🏆 Milestone updated: {detection_type} → {data[detection_type]}")

# Example usage:
# update_milestones("ip_detections")
# update_milestones("phishing_detections")
