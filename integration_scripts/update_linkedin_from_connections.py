#!/usr/bin/env python3
import sqlite3

matches = [
    ("Alexander Watson", "https://www.linkedin.com/in/alexander-watson-021a1025"),  # Alexander Watson - exact
    ("Ali Bin Shahid", "https://www.linkedin.com/in/alibinshahid"),  # Ali Bin Shahid - exact
    ("Amanda Joy Ravenhill", "https://www.linkedin.com/in/amandaravenhill"),  # Amanda Joy Ravenhill - exact
    ("Andrea Miller", "https://www.linkedin.com/in/andrea-miller-94b904122"),  # Andrea Miller - exact
    ("Andrew Atencia", "https://www.linkedin.com/in/andrew-atencia-7bba152a0"),  # Andrew Atencia - exact
    ("Apryle Schneeberger", "https://www.linkedin.com/in/apryle-schneeberger"),  # Apryle Schneeberger - exact
    ("Daphne Amory", "https://www.linkedin.com/in/daphne-amory"),  # Daphne Amory - exact
    ("Haley Kraczek", "https://www.linkedin.com/in/haley-k-36446515b"),  # Haley Kraczek - exact
    ("Jeremy Epstein", "https://www.linkedin.com/in/jeremyepstein"),  # Jeremy Epstein - exact
    ("John Magugu", "https://www.linkedin.com/in/john-westley-magugu-3ba3a1123"),  # John Westley Magugu - partial
    ("John Perlin", "https://www.linkedin.com/in/john-perlin-3b162b17"),  # John Perlin - exact
    ("Karim Camara", "https://www.linkedin.com/in/abdoul-karim-camara-3136b8144"),  # Abdoul Karim CAMARA - partial
    ("Kathleen Groppe", "https://www.linkedin.com/in/kathleen-groppe-48a907bb"),  # Kathleen Groppe - exact
    ("Luc Lendrum", "https://www.linkedin.com/in/luc-lendrum"),  # Luc Lendrum - exact
    ("Majd Thabit", "https://www.linkedin.com/in/majd-thabit-10b2181a"),  # Majd Thabit - exact
    ("Mark Frederiks", "https://www.linkedin.com/in/markfrederiks"),  # Mark Frederiks - exact
    ("Michael Haupt", "https://www.linkedin.com/in/michaelhaupt"),  # Michael Haupt - exact
    ("Richard Lukens", "https://www.linkedin.com/in/richard-lukens-5603"),  # Richard Lukens - exact
    ("Sarah Scherr", "https://www.linkedin.com/in/sara-scherr-0968a316"),  # Sara Scherr - partial
]

conn = sqlite3.connect("FathomInventory/fathom_emails.db")
cursor = conn.cursor()

for name, url in matches:
    cursor.execute("UPDATE participants SET linkedin_url = ? WHERE name = ?", (url, name))
    if cursor.rowcount > 0:
        print(f"✅ {name}")

conn.commit()
conn.close()
