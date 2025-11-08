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
    journal_pdfs = [
        {"title": "Computer Engineering Journal 2024", "file": "ce_journal_2024.pdf"},
        {"title": "Mechanical Research Papers 2023", "file": "mech_research_2023.pdf"},
    ]
    return render_template('ejournals.html', journal_pdfs=journal_pdfs)
# ---------- STAFF PAGE ----------
@app.route('/staff')
def staff():
    staff_members = [
        {
            "name": "Dr. Neha Sharma",
            "degree": "PhD in Library Science",
            "role": "Head Librarian",
            "email": "neha.sharma@ldce.ac.in",
            "phone": "+91 98765 43210",
            "work": "Library administration, policy decisions, acquisitions",
            "photo": "staff/neha.jpg"
        },
        {
            "name": "Mr. Rakesh Patel",
            "degree": "MLIS",
            "role": "Assistant Librarian",
            "email": "rakesh.patel@ldce.ac.in",
            "phone": "+91 91234 56789",
            "work": "Book issuance, cataloging, student help desk",
            "photo": "staff/rakesh.jpg"
        },
        {
            "name": "Ms. Priya Desai",
            "degree": "BLIS",
            "role": "Technical Assistant",
            "email": "priya.desai@ldce.ac.in",
            "phone": "+91 98989 55667",
            "work": "Digital library, databases, technical support",
            "photo": "staff/priya.jpg"
        },
        {
            "name": "Mr. Arvind Kumar",
            "degree": "BLIS",
            "role": "Library Assistant",
            "email": "arvind.kumar@ldce.ac.in",
            "phone": "+91 90909 33445",
            "work": "Physical book management, reading hall support",
            "photo": "staff/arvind.jpg"
        },
        {
            "name": "Ms. Komal Shah",
            "degree": "MLIS",
            "role": "Acquisition Specialist",
            "email": "komal.shah@ldce.ac.in",
            "phone": "+91 99887 66432",
            "work": "New arrivals, publisher coordination, procurement",
            "photo": "staff/komal.jpg"
        },
        {
            "name": "Mr. Jignesh Parmar",
            "degree": "BLIS",
            "role": "Circulation Manager",
            "email": "jignesh.parmar@ldce.ac.in",
            "phone": "+91 99112 44556",
            "work": "Issue-return operations, overdue management",
            "photo": "staff/jignesh.jpg"
        }
    ]
    
    return render_template('staff.html', staff=staff_members)


# ---------- DONATION FORM ----------
@app.route('/donation', methods=["GET", "POST"])
def donation_form():
    if request.method == "POST":
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        book_name = request.form.get('book_name')
        author_name = request.form.get('author_name')
        isbn = request.form.get('isbn')
        message = request.form.get('message')

        # Insert donation without date column
        with get_db_connection() as conn:
            conn.execute("""
            INSERT INTO suggestions 
            (name, student_id, email, message, type, book_name, author_name, isbn)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, student_id, email, message, "donation", book_name, author_name, isbn))

        flash("✅ Donation request submitted successfully!")
        return redirect(url_for('donation_form'))

    return render_template("donation_form.html")

# ---------- LOST BOOK FORM ----------
@app.route('/lost_book', methods=["GET", "POST"])
def lost_book_form():
    if request.method == "POST":
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        book_name = request.form.get('book_name')
        message = request.form.get('message')

        # Insert lost_book without date column
        with get_db_connection() as conn:
            conn.execute("""
                INSERT INTO suggestions 
                (name, student_id, email, book_name, author_name, isbn, message, type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (name, student_id, email, book_name, '', '', message, "lost_book"))

        flash("❗ Lost book report submitted successfully!")
        return redirect(url_for('lost_book_form'))

    return render_template("lost_book_form.html")

# ---------- SUGGESTION FORM ----------
@app.route('/suggestion', methods=["GET", "POST"])
def suggestion_form():
    if request.method == "POST":
        name = request.form.get('name')
        student_id = request.form.get('student_id')
        email = request.form.get('email')
        message = request.form.get('message')

        with get_db_connection() as conn:
            conn.execute(
                "INSERT INTO suggestions (name, student_id, email, message, type) VALUES (?, ?, ?, ?, ?)",
                (name, student_id, email, message, "suggestion")
            )

        flash("✅ Suggestion submitted!")
        return redirect(url_for('suggestion_form'))

    return render_template("suggestion_form.html")

# ---------- STUDENT DASHBOARD ----------
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
    results = []
    if query:
        conn = get_db_connection()
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
        try:
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO reservations (title, student_name, student_id, reservation_date)
                    VALUES (?, ?, ?, ?)
                """, (title, student_name, student_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            flash(f"✅ Reservation for '{title}' submitted successfully! A librarian will contact you.", 'success')
        except Exception as e:
            flash(f"❌ Database error: Could not process reservation. ({e})", 'error')

    return redirect(url_for('student_dashboard') + '#reserve')

# ---------- ADMIN DASHBOARD ----------
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC").fetchall()
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    reservations = conn.execute("SELECT * FROM reservations ORDER BY reservation_date DESC").fetchall()
    donations = conn.execute("SELECT * FROM suggestions WHERE type='donation' ORDER BY ROWID DESC").fetchall()
    lost_books = conn.execute("SELECT * FROM suggestions WHERE type='lost_book' ORDER BY ROWID DESC").fetchall()
    suggestions = conn.execute("SELECT * FROM suggestions WHERE type='suggestion' ORDER BY ROWID DESC").fetchall()
    config_rows = conn.execute("SELECT key, value FROM config").fetchall()
    config = {row['key']: row['value'] for row in config_rows}
    conn.close()

    return render_template(
        'admin.html',
        books=books,
        faqs=faqs,
        reservations=reservations,
        donations=donations,
        lost_books=lost_books,
        suggestions=suggestions,  # added for live suggestions
        config=config,
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
        try:
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO new_arrivals (title, author, isbn, arrival_date)
                    VALUES (?, ?, ?, ?)
                """, (title, author, isbn, arrival_date))
            flash(f"✅ Book '{title}' added successfully to New Arrivals!", 'success')
        except sqlite3.IntegrityError:
            flash(f"❌ Error: Book with ISBN {isbn} might already exist.", 'error')
        except Exception as e:
            flash(f"❌ Database error: {e}", 'error')

    return redirect(url_for('admin_dashboard'))

# ---------- ADMIN: UPDATE CONFIG ----------
@app.route('/admin/update-config', methods=['POST'])
def admin_update_config():
    regular_timing = request.form.get('regular_timing')
    special_timing = request.form.get('special_timing')
    announcement = request.form.get('announcement')

    try:
        with get_db_connection() as conn:
            conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('regular_timing', regular_timing))
            conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('special_timing', special_timing))
            conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('announcement', announcement))
        flash("✅ Library Timings and Announcement updated successfully!", 'success')
    except Exception as e:
        flash(f"❌ Database error during config update: {e}", 'error')

    return redirect(url_for('admin_dashboard') + '#timings')

# ---------- MAIN ----------
if __name__ == '__main__':
    app.run(debug=True) 