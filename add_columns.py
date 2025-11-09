# ✅ add_columns.py (improved version)
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE suggestions ADD COLUMN email TEXT")
    print("✅ 'email' column added successfully!")
except sqlite3.OperationalError as e:
    print("⚠", e)

conn.commit()
conn.close()
