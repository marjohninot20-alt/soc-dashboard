from incident_db import insert_incident
from datetime import datetime

insert_incident(
    timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    source="manual_test",
    indicator="Matched IP: 192.168.1.10",
    severity="Medium",
    action="Simulated block"
)

print("✅ Test incident inserted into database.")
