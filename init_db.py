import sqlite3
from datetime import datetime

# Connect to the database (creates it if it doesn’t exist)
connection = sqlite3.connect('database.db')

# ***************************************************************
# FIX: Add UTF-8 encoding to avoid UnicodeDecodeError
# ***************************************************************
with open('schema.sql', encoding='utf-8') as f:
    connection.executescript(f.read())

cur = connection.cursor()

# ----------------- New Arrivals (Books) -----------------
# Use today’s date in YYYY-MM-DD format
today_date = datetime.now().strftime('%Y-%m-%d')

cur.execute("INSERT INTO new_arrivals (title, author, isbn, arrival_date) VALUES (?, ?, ?, ?)",
            ('Python for Data Analysis', 'Wes McKinney', '9781491957662', today_date))

cur.execute("INSERT INTO new_arrivals (title, author, isbn, arrival_date) VALUES (?, ?, ?, ?)",
            ('Machine Learning Design Patterns', 'Valliappa Lakshmanan', '9781098115712', today_date))

cur.execute("INSERT INTO new_arrivals (title, author, isbn, arrival_date) VALUES (?, ?, ?, ?)",
            ('The Lord of the Rings', 'J.R.R. Tolkien', '9780547928286', today_date))

# ----------------- FAQs (Frequently Asked Questions) -----------------

cur.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)",
            ('What are the library\'s official opening hours?',
             'The library is open from 9:00 AM to 8:00 PM, Monday to Friday, and 10:00 AM to 5:00 PM on Saturdays.'))

cur.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)",
            ('How many books can I issue at once?',
             'Students can issue a maximum of 4 books, and faculty members can issue up to 10 books.'))

cur.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)",
            ('What is the standard return period for issued books?',
             'Issued books must be returned within 15 days from the date of issue. Overdue fines may apply.'))

cur.execute("INSERT INTO faqs (question, answer) VALUES (?, ?)",
            ('Is there Wi-Fi available for students?',
             'Yes, high-speed Wi-Fi is available throughout the library premises for all registered students and staff.'))

# Commit the changes and close the connection
connection.commit()
connection.close()

print("Database 'database.db' successfully initialized with initial data.")
