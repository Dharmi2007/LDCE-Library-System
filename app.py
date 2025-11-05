from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
app = Flask(__name__)
# REQUIRED for flash messages and session security
app.config['SECRET_KEY'] = 'your_hackathon_secret_key_12345'
DATABASE = 'database.db'

# ---------- DATABASE CONNECTION UTILITY ----------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- STUDENT DASHBOARD (Renders index.html) ----------
# ---------- SEARCH FEATURE ----------
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

@app.route('/', methods=['GET'])
def student_dashboard():
    conn = get_db_connection()
    
    # 1. Fetch Dynamic Data from DB
    new_arrivals = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC LIMIT 8").fetchall()
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    
    # Fetch Config (Timings/Announcement)
    config_rows = conn.execute("SELECT key, value FROM config").fetchall()
    config = {row['key']: row['value'] for row in config_rows}
    
    conn.close()

    # Default/Static data (Use config data where possible)
    timings = {
        "Mon - Fri": config.get('regular_timing', '9 AM - 6 PM'),
        "Saturday": config.get('special_timing', '9 AM - 1 PM'),
        "Sunday": "Closed"
    }
    external_links = {
        "LDCE Official Website": "https://ldce.ac.in",
        "NDL - Digital Library": "https://ndl.iitkgp.ac.in",
        "ONOS Portal": "https://ldce.example.com/onos" # Placeholder
    }
    announcement_message = config.get('announcement')

    # !!! CRITICAL FIX: Render index.html for the student view !!!
    return render_template(
        'index.html',
        new_arrivals=new_arrivals,
        faqs=faqs,
        timings=timings,
        external_links=external_links,
        announcement_message=announcement_message,
        current_year=datetime.now().year
    )

# ---------- RESERVE BOOK POST ROUTE ----------
@app.route('/reserve', methods=['POST'])
def reserve_book():
    title = request.form.get('title')
    student_name = request.form.get('student_name')
    student_id = request.form.get('student_id')
    
    if not all([title, student_name, student_id]):
        flash("⚠️ All fields are required to reserve a book.", 'error')
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
            
    # Redirect back to the homepage, targeting the reservation section
    return redirect(url_for('student_dashboard') + '#reserve')


# ---------- ADMIN DASHBOARD (Renders admin.html) ----------
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    conn = get_db_connection()
    
    # Fetch all books for the table view
    books = conn.execute("SELECT * FROM new_arrivals ORDER BY arrival_date DESC").fetchall()
    
    # Fetch current config for the Timings tab
    config_rows = conn.execute("SELECT key, value FROM config").fetchall()
    config = {row['key']: row['value'] for row in config_rows}
    
    # Fetch FAQs for the FAQ tab
    faqs = conn.execute("SELECT * FROM faqs").fetchall()
    
    conn.close()
    
    # !!! CRITICAL FIX: Render admin.html for the admin view !!!
    return render_template('admin.html',
                       books=books,
                       config=config,
                       faqs=faqs,
                       datetime=datetime)

# ---------- ADMIN POST ROUTES ----------

@app.route('/admin/add-book', methods=['POST'])
def admin_add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    isbn = request.form.get('isbn')
    arrival_date = request.form.get('arrival_date')

    if not all([title, author, isbn, arrival_date]):
        flash("⚠️ Please fill in all fields to add a book.", 'error')
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
            
    # Redirect back to the admin dashboard, focusing on the books tab
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/update-config', methods=['POST'])
def admin_update_config():
    # This route handles updates for Timings and Announcements
    regular_timing = request.form.get('regular_timing')
    special_timing = request.form.get('special_timing')
    announcement = request.form.get('announcement')

    conn = get_db_connection()
    try:
        # Use INSERT OR REPLACE to update existing key or insert a new one
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('regular_timing', regular_timing))
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('special_timing', special_timing))
        conn.execute("INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)", ('announcement', announcement))
        conn.commit()
        flash("✅ Library Timings and Announcement updated successfully!", 'success')
    except Exception as e:
        flash(f"❌ Database error during config update: {e}", 'error')
    finally:
        conn.close()
        
    return redirect(url_for('admin_dashboard') + '#timings') # Target the timings tab


# --- MAIN ---
if __name__ == '__main__':
    app.run(debug=True) 