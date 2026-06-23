from flask import Flask, render_template, request

app = Flask(__name__)

# Basic Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Static "All Books" Route (No DB connection)
@app.route('/all-books')
def all_books():
    # Since we removed the DB, we define the data directly here
    books = [
        {"title": "The Hunger Games", "author": "Suzanne Collins", "genre": "Science Fiction, Adventure, Thriller", "rating": 4.5, "desc": "Teens fight to the death in a dystopian society."},
        {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "genre": "Fantasy, Adventure", "rating": 4.8, "desc": "A young wizard discovers his magical heritage."},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Classic, Drama", "rating": 4.8, "desc": "A lawyer defends a Black man in the American South."},
        {"title": "Atomic Habits", "author": "James Clear", "genre": "Self-Help, Inspirational", "rating": 4.8, "desc": "Tiny changes that lead to remarkable results."},
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy, Adventure", "rating": 4.7, "desc": "Bilbo Baggins embarks on an unexpected journey."},
        {"title": "1984", "author": "George Orwell", "genre": "Science Fiction, Classic", "rating": 4.7, "desc": "A dystopian society under constant government surveillance."},
        {"title": "Sherlock Holmes", "author": "Arthur Conan Doyle", "genre": "Mystery, Classic", "rating": 4.7, "desc": "The world's greatest detective solves implausible cases."},
        {"title": "Dune", "author": "Frank Herbert", "genre": "Science Fiction, Adventure", "rating": 4.6, "desc": "A noble family controls the desert planet Arrakis."},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance, Classic", "rating": 4.6, "desc": "Elizabeth Bennet navigates love and social class."},
        {"title": "Sapiens", "author": "Yuval Noah Harari", "genre": "Non-Fiction, History", "rating": 4.4, "desc": "A brief history of humankind."},
        {"title": "The Da Vinci Code", "author": "Dan Brown", "genre": "Mystery, Thriller", "rating": 4.3, "desc": "A Harvard professor unravels a religious mystery."},
        {"title": "The Alchemist", "author": "Paulo Coelho", "genre": "Adventure, Inspirational", "rating": 4.3, "desc": "A shepherd boy travels in search of treasure."}
    ]
  return render_template('all_books.html', books=books)

if __name__ == "__main__":
    app.run()  
    