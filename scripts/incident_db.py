import sqlite3
from datetime import datetime

# ✅ Create the incidents table with zone support
def create_incident_table():
    conn = sqlite3.connect("reports/incidents.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            source TEXT,
            indicator TEXT,
            severity TEXT,
            action TEXT,
            zone TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("✅ incidents.db created with proper schema.")

# ✅ Insert incident with zone tagging
def insert_incident(timestamp, source, indicator, severity, action, zone):
    conn = sqlite3.connect("reports/incidents.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO incidents (timestamp, source, indicator, severity, action, zone)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, source, indicator, severity, action, zone))
    conn.commit()
    conn.close()

# ✅ Optional test insert (can be removed later)
def test_insert():
    insert_incident(
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        source="Test Source",
        indicator="Test Indicator",
        severity="Low",
        action="Simulated block",
        zone="Test Zone"
    )

if __name__ == "__main__":
    create_incident_table()
    test_insert()
