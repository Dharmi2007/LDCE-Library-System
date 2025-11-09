import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create suggestions table compatible with app.py
cursor.execute("""
CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    suggestion TEXT NOT NULL
);
""")

conn.commit()
conn.close()
print("✅ Table created or already exists.")
