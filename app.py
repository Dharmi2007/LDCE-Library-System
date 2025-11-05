from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# ---------- STUDENT DASHBOARD ----------
@app.route('/', methods=['GET', 'POST'])
def student_dashboard():
    conn = get_db_connection()

    # Fetch New Arrivals
    new_arrivals = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC").fetchall()

    # Fetch FAQs
    faqs = conn.execute("SELECT * FROM faqs").fetchall()

    conn.close()

    # Static data (timings + external links)
    timings = {
        "Monday": "9 AM - 6 PM",
        "Tuesday": "9 AM - 6 PM",
        "Wednesday": "9 AM - 6 PM",
        "Thursday": "9 AM - 6 PM",
        "Friday": "9 AM - 6 PM",
        "Saturday": "9 AM - 1 PM",
        "Sunday": "Closed"
    }

    external_links = {
        "LDCE Official Website": "https://ldce.ac.in",
        "Digital Library": "https://ndl.iitkgp.ac.in"
    }

    # ---------- Reserve Book ----------
    if request.method == 'POST':
        title = request.form.get('title')
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')

        if title and student_name and student_id:
            conn = get_db_connection()
            conn.execute("""
                INSERT INTO reservations (title, student_name, student_id, reservation_date)
                VALUES (?, ?, ?, ?)
            """, (title, student_name, student_id, datetime.now()))
            conn.commit()
            conn.close()
        return redirect(url_for('student_dashboard'))

    return render_template(
        'admin.html',  # student page design
        new_arrivals=new_arrivals,
        faqs=faqs,
        timings=timings,
        external_links=external_links,
        current_year=datetime.now().year
    )


# ---------- ADMIN DASHBOARD ----------
@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    conn = get_db_connection()
    admin_message = None

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        arrival_date = request.form.get('arrival_date')

        if title and author and isbn and arrival_date:
            conn.execute("""
                INSERT INTO new_arrivals (title, author, isbn, arrival_date)
                VALUES (?, ?, ?, ?)
            """, (title, author, isbn, arrival_date))
            conn.commit()
            admin_message = f"✅ '{title}' added successfully!"
        else:
            admin_message = "⚠ Please fill in all fields!"

    # Fetch updated books
    books = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC").fetchall()
    conn.close()

    return render_template('index.html', books=books, admin_message=admin_message)


# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True)