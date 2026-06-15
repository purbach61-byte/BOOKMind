import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'books.db')

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    #ADD THIS LINE HERE TO CLEAR THE OLD STRUCTURE:
    cursor.execute("DROP TABLE IF EXISTS books")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            rating REAL NOT NULL,
            description TEXT
        )
    ''')

    # Expanded book list covering different genres and all rating tiers
    sample_books = [
        # --- Fantasy ---
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 4.8, "A glorious adventure in Middle-earth."),
        ("Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "Fantasy", 4.7, "The magical journey of a young wizard begins."),
        ("The Name of the Wind", "Patrick Rothfuss", "Fantasy", 4.5, "The tale of a notoriously gifted wizard."),
        
        # --- Science Fiction ---
        ("Dune", "Frank Herbert", "Science Fiction", 4.7, "An epic sci-fi masterpiece set on the desert planet Arrakis."),
        ("Project Hail Mary", "Andy Weir", "Science Fiction", 4.9, "An astronaut tries to save Earth alongside an alien ally."),
        ("The Martian", "Andy Weir", "Science Fiction", 4.6, "An astronaut's solo survival mission stranded on Mars."),
        ("Neuromancer", "William Gibson", "Science Fiction", 3.9, "The classic cyberpunk novel that defined the matrix generation."),

        # --- Mystery & Thriller ---
        ("Sherlock Holmes", "Arthur Conan Doyle", "Mystery", 4.6, "Classic detective tales from Baker Street."),
        ("The Silent Patient", "Alex Michaelides", "Thriller", 4.4, "A shocking psychological thriller about a woman's hidden secrets."),
        ("Gone Girl", "Gillian Flynn", "Thriller", 4.1, "A dark and twisting tale of a marriage gone completely wrong."),
        ("The Da Vinci Code", "Dan Brown", "Mystery", 3.8, "A high-stakes puzzle race through secret societies and art history."),

        # --- Romance ---
        ("Pride and Prejudice", "Jane Austen", "Romance", 4.5, "The classic romantic comedy of manners and misunderstandings."),
        ("The Fault in Our Stars", "John Green", "Romance", 4.3, "A beautifully heartbreaking love story between two teenagers."),
        ("Normal People", "Sally Rooney", "Romance", 3.7, "A nuanced look at the complex relationship between two young adults."),
        ("The Notebook", "Nicholas Sparks", "Romance", 4.0, "An enduring and passionate tale of lifelong love.")
    ]

    # Clear out any previous traces and insert the robust dataset
    cursor.execute("DELETE FROM books")
    cursor.executemany(
        "INSERT INTO books (title, author, genre, rating, description) VALUES (?, ?, ?, ?, ?)", 
        sample_books
    )
    
    conn.commit()
    conn.close()
    print("🎉 Database successfully updated with a huge collection of books across all ratings!")

if __name__ == "__main__":
    seed_database()