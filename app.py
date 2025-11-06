from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_hackathon_secret_key_12345'
DATABASE = 'database.db'


# ---------- DATABASE CONNECTION ----------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- STUDENT DASHBOARD ----------
@app.route('/guidelines')
def guidelines():
    return render_template('guidelines.html')
@app.route('/faqs')
def faqs():
    faqs_list = [
        {"question": "How can I issue a book?", "answer": "Visit the circulation desk with your student ID card."},
        {"question": "What is the book return period?", "answer": "Books must be returned within 14 days."},
        {"question": "Can I renew books online?", "answer": "Currently, renewals are available only at the library counter."},
        {"question": "What happens if I lose a book?", "answer": "You must replace the same book or pay the replacement cost."},
    ]
    return render_template('faqs.html', faqs=faqs_list)
@app.route('/ejournals')
def ejournals():
    # Example PDFs (add more as needed) – place files inside /static/journals/
    journal_pdfs = [
        {"title": "Computer Engineering Journal 2024", "file": "ce_journal_2024.pdf"},
        {"title": "Mechanical Research Papers 2023", "file": "mech_research_2023.pdf"},
    ]

    return render_template('ejournals.html', journal_pdfs=journal_pdfs)




@app.route('/', methods=['GET'])
def student_dashboard():
    conn = get_db_connection()
    new_arrivals = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC LIMIT 8").fetchall()
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    config_rows = conn.execute("SELECT key, value FROM config").fetchall()
    config = {row['key']: row['value'] for row in config_rows}
    conn.close()

    timings = {
        "Mon - Fri": config.get('regular_timing', '9 AM - 6 PM'),
        "Saturday": config.get('special_timing', '9 AM - 1 PM'),
        "Sunday": "Closed"
    }
    external_links = {
        "LDCE Official Website": "https://ldce.ac.in",
        "NDL - Digital Library": "https://ndl.iitkgp.ac.in",
        "ONOS Portal": "https://ldce.example.com/onos"
    }
    announcement_message = config.get('announcement')

    return render_template(
        'index.html',
        new_arrivals=new_arrivals,
        faqs=faqs,
        timings=timings,
        external_links=external_links,
        announcement_message=announcement_message,
        current_year=datetime.now().year
    )


# ---------- SEARCH ----------
@app.route('/search')
def search():
    query = request.args.get('query', '').strip()
    conn = get_db_connection()
    results = []
    if query:
        results = conn.execute("""
            SELECT * FROM new_arrivals 
            WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ?
        """, (f"%{query}%", f"%{query}%", f"%{query}%")).fetchall()
    conn.close()
    return render_template('search_result.html', query=query, results=results)


# ---------- RESERVE BOOK ----------
@app.route('/reserve', methods=['POST'])
def reserve_book():
    title = request.form.get('title')
    student_name = request.form.get('student_name')
    student_id = request.form.get('student_id')

    if not all([title, student_name, student_id]):
        flash("⚠ All fields are required to reserve a book.", 'error')
    else:
        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO reservations (title, student_name, student_id, reservation_date)
                VALUES (?, ?, ?, ?)
            """, (title, student_name, student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            flash(f"✅ Reservation for '{title}' submitted successfully! A librarian will contact you.", 'success')
        except Exception as e:
            flash(f"❌ Database error: Could not process reservation. ({e})", 'error')
        finally:
            conn.close()

    return redirect(url_for('student_dashboard') + '#reserve')


# ---------- ADMIN DASHBOARD ----------
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC").fetchall()
    config_rows = conn.execute("SELECT key, value FROM config").fetchall()
    config = {row['key']: row['value'] for row in config_rows}
    faqs = conn.execute("SELECT * FROM faqs").fetchall()

    # ✅ NEW: Fetch student reservations
    reservations = conn.execute("""
        SELECT * FROM reservations ORDER BY reservation_date DESC
    """).fetchall()

    conn.close()
    return render_template(
        'admin.html',
        books=books,
        config=config,
        faqs=faqs,
        reservations=reservations,
        datetime=datetime
    )


# ---------- ADMIN: ADD BOOK ----------
@app.route('/admin/add-book', methods=['POST'])
def admin_add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    arrival_date = request.form.get('arrival_date')

    if not all([title, author, isbn, arrival_date]):
        flash("⚠ Please fill in all fields to add a book.", 'error')
    else:
        conn = get_db_connection()
        try:
            conn.execute("""
                INSERT INTO new_arrivals (title, author, isbn, arrival_date)
                VALUES (?, ?, ?, ?)
            """, (title, author, isbn, arrival_date))
            conn.commit()
            flash(f"✅ Book '{title}' added successfully to New Arrivals!", 'success')
        except sqlite3.IntegrityError:
            flash(f"❌ Error: Book with ISBN {isbn} might already exist.", 'error')
        except Exception as e:
            flash(f"❌ Database error: {e}", 'error')
        finally:
            conn.close()

    return redirect(url_for('admin_dashboard'))


# ---------- ADMIN: UPDATE CONFIG ----------
@app.route('/admin/update-config', methods=['POST'])
def admin_update_config():
    regular_timing = request.form.get('regular_timing')
    special_timing = request.form.get('special_timing')
    announcement = request.form.get('announcement')

    conn = get_db_connection()
    try:
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('regular_timing', regular_timing))
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('special_timing', special_timing))
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('announcement', announcement))
        conn.commit()
        flash("✅ Library Timings and Announcement updated successfully!", 'success')
    except Exception as e:
        flash(f"❌ Database error during config update: {e}", 'error')
    finally:
        conn.close()

    return redirect(url_for('admin_dashboard') + '#timings')


# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True)