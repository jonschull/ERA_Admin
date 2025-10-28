#!/usr/bin/env python3
import sqlite3

matches = [
    ("Laura Perez Arce", "https://www.linkedin.com/in/vivasierragorda/"),  # Laura Perez-Arce (94%)
    ("Sarah Scherr", "https://linkedin.com/in/sara-scherr-0968a316"),  # Sara Scherr (96%)
]

conn = sqlite3.connect("FathomInventory/fathom_emails.db")
cursor = conn.cursor()

for name, url in matches:
    cursor.execute("UPDATE participants SET linkedin_url = ? WHERE name = ?", (url, name))
    print(f"✅ {name}: {url}")

conn.commit()
conn.close()
