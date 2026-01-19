-- schema.sql

-- Drop existing tables
DROP TABLE IF EXISTS new_arrivals;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS faqs;
DROP TABLE IF EXISTS config;
DROP TABLE IF EXISTS staff;
DROP TABLE IF EXISTS suggestions;

-- 1. Table to store newly arrived books (New Arrivals)
CREATE TABLE new_arrivals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    arrival_date DATE NOT NULL
);

-- 2. Table to store user reservation requests
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    reservation_date TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now'))
);

-- 3. Table to store Frequently Asked Questions (FAQs)
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

-- 4. Config Table for Timings and Announcement
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

-- 5. Staff Login Table (updated)
CREATE TABLE staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    name TEXT NOT NULL,         -- Full Name
    photo TEXT                  -- Photo filename (store in /static/images/staff/)
);

-- Insert a default staff account with name and photo
INSERT OR IGNORE INTO staff (username, password, name, photo)
VALUES ('staffadmin', 'lib@123', 'Library Admin', 'default_staff.png');


-- 6. Table for Suggestions, Donations, and Lost Books
CREATE TABLE suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    student_id TEXT,
    email TEXT,
    book_name TEXT,
    author_name TEXT,
    isbn TEXT,
    message TEXT
);


-- 7. Insert Default FAQs
INSERT INTO faqs (question, answer) VALUES 
('How can I check out a book?', 'Present your student ID and the book at the circulation desk during operating hours.'),
('What is the fine for late return?', 'The standard late fee is ₹5 per day, per book. Please return books on time!'),
('Can I access digital journals?', 'Yes, please use the ONOS Portal link on the homepage with your college credentials.');

-- 8. Insert Default Config (Timings & Announcement)
INSERT INTO config (key, value) VALUES 
('regular_timing', '9:00 AM - 6:00 PM (Mon-Fri)'),
('special_timing', '9:00 AM - 1:00 PM (Sat)'),
('announcement', 'Welcome to the new LDCE Central Library digital portal! We are currently closed on Sunday.');

-- 9. Insert Example New Arrivals
INSERT INTO new_arrivals (title, author, isbn, arrival_date) VALUES
('Hackathon Guide to Success', 'Dr. S S Pathan', '9781001001001', '2025-10-25'),
('Advanced Python for AI', 'Guido van Rossum', '9781001001002', '2025-10-30'); 