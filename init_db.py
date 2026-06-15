import sqlite3
# This will create the books.db file automatically
conn = sqlite3.connect('books.db')
#Create the database table structure
conn.execute('''CREATE TABLE IF NOT EXISTS books
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 genre TEXT NOT NULL,
                 rating REAL NOT NULL)''')
#The sample book data to insert
sample_books = [
    ('The Great Gatsby', 'Fiction', 4.5),
    ('To Kill a Mockingbird', 'Fiction', 4.8),
    ('1984', 'Dystopian', 4.7),
    ('Pride and Prejudice', 'Romance', 4.6),
    ('The Catcher in the Rye', 'Fiction', 4.2)
]                 
conn.executemany('INSERT INTO books (title, genre, rating) VALUES (?, ?, ?)', sample_books)
conn.commit()
conn.close()
print("Database initialized successfully.")