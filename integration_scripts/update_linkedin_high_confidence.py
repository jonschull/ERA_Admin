#!/usr/bin/env python3
import sqlite3

matches = [
    ("Nima Schei", "https://www.linkedin.com/in/nima-schei-md-0288a824"),  # Nima Schei, MD - 2 name parts match
    ("Cassandra Kiki Ami", "https://www.linkedin.com/in/cassandra-kiki-ami-shaffer-67434398"),  # Cassandra Kiki Ami Shaffer - 3 name parts match
    ("Aviv Green", "https://www.linkedin.com/in/david-green-3115a5a"),  # David Green - Same last name
    ("Lauren Miller", "https://www.linkedin.com/in/arman-miller-213527150"),  # Arman Miller - Same last name
    ("Fadja Robert", "https://www.linkedin.com/in/kiama-robert-20a255a8"),  # KIAMA Robert - Same last name
    ("Myra Jackson", "https://www.linkedin.com/in/guy-jackson-7931a2b"),  # Guy Jackson - Same last name
    ("Consolata Gitau", "https://www.linkedin.com/in/consolata-gathoni-gitau-ecologist-rangeland-scientist-ecologist-acoustician"),  # Consolata Gathoni - Unique first name match
    ("Juan Bernal", "https://www.linkedin.com/in/josedanilobernal"),  # Jose Danilo Bernal - Same last name
    ("Ivan Owen", "https://www.linkedin.com/in/jen-owen-719201133"),  # Jen Owen - Same last name
    ("Angelique Garcia", "https://www.linkedin.com/in/ritzagarcia"),  # Maritza Garcia - Same last name
    ("Poyom Boydell", "https://www.linkedin.com/in/poyom-riles"),  # Poyom Riles - Unique first name match
]

conn = sqlite3.connect("FathomInventory/fathom_emails.db")
cursor = conn.cursor()

for name, url in matches:
    cursor.execute("UPDATE participants SET linkedin_url = ? WHERE name = ?", (url, name))
    if cursor.rowcount > 0:
        print(f"✅ {name}")

conn.commit()
conn.close()
