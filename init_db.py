import sqlite3
# This will create the books.db file automatically
conn = sqlite3.connect('books.db')
#Create the database table structure
conn.execute('''CREATE TABLE IF NOT EXISTS books
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 author TEXT NOT NULL,
                 genre TEXT NOT NULL,
                 rating REAL,
                 description TEXT
                 )''')
#The sample book data to insert
sample_books = [
    ('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 4.5, 'A classic American novel'),
    ('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 4.8, 'A gripping tale of racial injustice'),
    ('1984', 'George Orwell', 'Dystopian', 4.7, 'A dystopian social science fiction novel'),
    ('Pride and Prejudice', 'Jane Austen', 'Romance', 4.6, 'A romantic novel of manners'),
    ('The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 4.2, 'A controversial novel about teenage rebellion'),
    ('Digital Fortress', 'Dan Brown', 'Mystery, Tech', 4.2, 'Leisure read involving cryptographic systems'),
    ('Snow Crash', 'Neal Stephenson', 'Sci-Fi, Tech', 4.5, 'Leisure sci-fi classic exploring the metaverse'),
    ('The Girl with the Dragon Tattoo', 'Stieg Larsson', 'Mystery, Thriller', 4.4, 'Leisure mystery thriller'),
    ('Clean Code', 'Robert C. Martin', 'Technology, Programming', 4.7, 'Professional handbook for software engineers'),
    ('Sapiens', 'Yuval Noah Harari', 'History, Science', 4.6, 'Academic exploration of human history'),
    ('Harry Potter (Book 1)', 'J.K. Rowling', 'Fantasy, Adventure', 4.8, 'Leisure fantasy adventure book'),
    ('Atomic Habits', 'James Clear', 'Self-Help, Psychology', 4.5, 'Self-help book focused on habit building'),
    ('The Alchemist', 'Paulo Coelho', 'Philosophy, Fiction', 4.3, 'Leisure philosophical novel')
]               
conn.executemany('INSERT INTO books (title, author, genre, rating, description) VALUES (?, ?, ?, ?, ?)', sample_books)
conn.commit()
conn.close()
print("Database initialized successfully.")