# ✅ add_columns.py (improved version)
import sqlite3
import time

def add_column(column_sql):
    try:
        c.execute(column_sql)
        print("✅ Added:", column_sql)
    except sqlite3.OperationalError as e:
        if "duplicate column" in str(e).lower():
            print("⚠ Column already exists, skipping:", column_sql)
        else:
            print("⚠ OperationalError:", e)
    except Exception as e:
        print("⚠ Error:", e)

# Try connecting with timeout (wait if locked)
for i in range(3):
    try:
        conn = sqlite3.connect("database.db", timeout=10)
        c = conn.cursor()
        break
    except sqlite3.OperationalError:
        print("Database is locked, retrying...")
        time.sleep(3)
else:
    raise Exception("❌ Could not connect to database.db (still locked)")

# Add donation-related columns safely
add_column("ALTER TABLE suggestions ADD COLUMN book_name TEXT;")
add_column("ALTER TABLE suggestions ADD COLUMN author_name TEXT;")
add_column("ALTER TABLE suggestions ADD COLUMN isbn TEXT;")
add_column("ALTER TABLE suggestions ADD COLUMN donation_date TEXT;")
add_column("ALTER TABLE suggestions ADD COLUMN message TEXT;")  # add message column

conn.commit()
conn.close()
print("🎉 Done - all columns added (if they didn’t already exist).")