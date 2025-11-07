-- schema.sql

-- Drop existing tables
DROP TABLE IF EXISTS new_arrivals;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS faqs;
DROP TABLE IF EXISTS config;

-- 1. Table to store newly arrived books (New Arrivals)
CREATE TABLE new_arrivals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    arrival_date DATE NOT NULL -- NO COMMA HERE
);

-- 2. Table to store user reservation requests
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    reservation_date TEXT NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now')) -- NO COMMA HERE
);

-- 3. Table to store Frequently Asked Questions (FAQs)
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL -- NO COMMA HERE
);

-- 4. Config Table for Timings and Announcement
CREATE TABLE config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL -- NO COMMA HERE
);


-- 5. Essential Initial Data Insertion

-- Insert Default FAQs
INSERT INTO faqs (question, answer) VALUES 
('How can I check out a book?', 'Present your student ID and the book at the circulation desk during operating hours.'),
('What is the fine for late return?', 'The standard late fee is ₹5 per day, per book. Please return books on time!'),
('Can I access digital journals?', 'Yes, please use the ONOS Portal link on the homepage with your college credentials.');

-- Insert Default Config/Timings/Announcement
INSERT INTO config (key, value) VALUES 
('regular_timing', '9:00 AM - 6:00 PM (Mon-Fri)'),
('special_timing', '9:00 AM - 1:00 PM (Sat)'),
('announcement', 'Welcome to the new LDCE Central Library digital portal! We are currently closed on Sunday.');

-- 6. Table to store suggestions, book donations, and lost book reports
DROP TABLE IF EXISTS suggestions;

CREATE TABLE suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT,
    type TEXT NOT NULL,        -- donation / lost_book / suggestion
    book_name TEXT,            -- For donation / lost_book
    author_name TEXT,          -- For donation
    isbn TEXT                  -- For donation
);

-- Insert Example New Arrivals
INSERT INTO new_arrivals (title, author, isbn, arrival_date) VALUES
('Hackathon Guide to Success', 'Dr. S S Pathan', '9781001001001', '2025-10-25'),
('Advanced Python for AI', 'Guido van Rossum', '9781001001002', '2025-10-30');