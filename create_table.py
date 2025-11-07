import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create donation/suggestions table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    email TEXT NOT NULL,
    book_name TEXT NOT NULL,
    author_name TEXT NOT NULL,
    isbn TEXT NOT NULL,
    date TEXT NOT NULL,
    type TEXT NOT NULL
);
""")

conn.commit()
conn.close()
print("✅ Table created or already exists.")