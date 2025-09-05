# 🛡️ SOC Dashboard Toolkit

A modular, Python-powered Security Operations Center (SOC) toolkit designed for real-world incident detection, log monitoring, phishing analysis, and milestone tracking. Built for tactical workflows, threat visibility, and operational readiness.

## 🚀 Features

- Real-time log monitoring (log_monitor.py)
- IOC matching and phishing detection (ioc_checker.py, phish_scan.py)
- Incident logging to SQLite (incident_db.py)
- Email inbox scanning and alerting (email_scanner.py, email_alert.py)
- Severity classification and zone tagging
- Streamlit-powered dashboard (soc_dashboard.py)
- Milestone tracking (milestone_tracker.py)
- Modular folder structure for data, logs, reports, and scripts

## 📁 Folder Structure

SOC-Toolkit/
├── data/               - IOC lists and indicators
├── emails/             - Sample email files
├── logs/               - Log files for testing
├── reports/            - Output logs, alerts, incidents.db
├── scripts/            - Python modules and dashboard
├── .gitignore          - Tactical exclusions
├── README.md           - Project overview
├── requirements.txt    - Dependencies

## 🔧 Setup Instructions

1. Clone the repo:

   git clone https://github.com/marjohninot20-alt/soc-dashboard.git
   cd soc-dashboard

2. Create a virtual environment:

   python -m venv venv
   venv\Scripts\activate  (Windows)

3. Install dependencies:

   pip install -r requirements.txt

4. Create a .env file in the root directory:

   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password

## 📧 Email Scanner Module

Scans unread Gmail messages, extracts indicators, classifies severity, logs incidents, and sends alerts.

Run with:

   python scripts/email_scanner.py

Output is saved to reports/email_scan_log.txt and incidents.db

## 📊 Dashboard

Launch the Streamlit dashboard:

   streamlit run scripts/soc_dashboard.py

Features:
- Severity summary
- Search and filter
- Incident table
- Bar chart visualization

## 🛡️ Security Notes

- Credentials are loaded from .env and excluded via .gitignore
- SQLite database (incidents.db) is optional and can be excluded from commits
- No sensitive data is exposed in the repository

## 🔗 Related Modules

- incident_db.py – inserts flagged incidents into the database
- email_alert.py – sends alert emails for high-severity threats
- milestone_tracker.py – tracks detection milestones
- phish_scan.py – scans logs for phishing indicators
- soc_dashboard.py – visualizes incidents in real time

---

Built by Marjohn for tactical SOC workflows. Clean, modular, and milestone-worthy.