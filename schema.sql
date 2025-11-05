-- Drop existing tables to ensure a clean slate and apply the new schema
DROP TABLE IF EXISTS new_arrivals;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS faqs;

-- Table to store newly arrived books in the library
CREATE TABLE new_arrivals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT NOT NULL,              -- Added ISBN column for tracking
    arrival_date DATE NOT NULL
);

-- Table to store user reservation requests
CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,             -- Title of the book requested
    student_name TEXT NOT NULL,
    student_id TEXT NOT NULL,
    reservation_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP -- Corrected column name used for sorting
);

-- Table to store Frequently Asked Questions (FAQs)
CREATE TABLE faqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);
