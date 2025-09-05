import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect("reports/incidents.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS incidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    indicator TEXT,
    severity TEXT,
    zone TEXT
)
""")

# Insert mock data
mock_data = [
    ("2025-09-01 10:15:00", "Suspicious login from 192.168.1.10", "High", "Zone A"),
    ("2025-09-02 14:30:00", "Phishing email detected", "Medium", "Zone B"),
    ("2025-09-03 09:45:00", "Malware signature match", "High", "Zone C"),
    ("2025-09-04 16:00:00", "Unusual outbound traffic", "Low", "Zone A"),
    ("2025-09-05 08:20:00", "Failed login attempt", "Medium", "Zone B")
]

cursor.executemany("""
INSERT INTO incidents (timestamp, indicator, severity, zone)
VALUES (?, ?, ?, ?)
""", mock_data)

conn.commit()
conn.close()

# Verify inserted data
conn = sqlite3.connect("reports/incidents.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM incidents")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()