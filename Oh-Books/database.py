import sqlite3
import requests

# Define the API endpoint to fetch book data
api_url = "https://api2.isbndb.com/book/"

# Make a request to the API to get book data
response = requests.get(api_url)
books_data = response.json()

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('books.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store book data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        isbn TEXT,
        publisher TEXT,
        date_published TEXT,
        pages INTEGER,
        overview TEXT,
        authors TEXT,
        my_rating REAL,
        my_reading_count INTEGER,
        is_owned INTEGER,
        is_wishlisted INTEGER
    )
''')
print("Table has been created")
# Iterate through the books data and insert it into the database
for book in books_data:
    cursor.execute('''
        INSERT INTO books 
        (title, title_long, isbn, isbn13, dewey_decimal, binding, publisher, language, date_published,
        edition, pages, dimensions, overview, image, msrp, excerpt, synopsis, authors, subjects, reviews,
        related_type, other_isbns)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        book['title'], book['title_long'], book['isbn'], book['isbn13'], book['dewey_decimal'],
        book['binding'], book['publisher'], book['language'], book['date_published'], book['edition'],
        book['pages'], book['dimensions'], book['overview'], book['image'], book['msrp'], book['excerpt'],
        book['synopsis'], ', '.join(book['authors']), ', '.join(book['subjects']),
        ', '.join(book['reviews']), book['related']['type'], ', '.join(f"{item['isbn']} - {item['binding']}" for item in book['other_isbns'])
    ))

# Commit changes and close connection
conn.commit()
conn.close()
