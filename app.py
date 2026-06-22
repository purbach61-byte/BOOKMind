import os
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# 🎯 ADD YOUR MONGODB ATLAS CONNECTION STRING HERE!
# Finish your signup on the website, get your driver URI string, and paste it right here:
MONGO_URI = "mongodb+srv://reader_user:purba2026@cluster0.kzpzltu.mongodb.net/?appName=Cluster0"

client = MongoClient(MONGO_URI)
db = client['bookmind_db']
books_collection = db['books']

# --- DATABASE SEEDING ENGINE ---
@app.route('/init-db')
def init_db():
    """Run this once on your local browser to load the data directly into your MongoDB Atlas cloud"""
    books_collection.delete_many({}) 
    
    sample_data = [
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
    
    books_collection.insert_many(sample_data)
    return "Extraordinary MongoDB Atlas Dataset Initialized Successfully! You can close this tab now."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/all-books')
def all_books():
    books = list(books_collection.find())
    return render_template('all_books.html', books=books)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_name = request.form.get('user_name', 'Reader')
    selected_genres = request.form.getlist('genres')
    try:
        min_rating = float(request.form.get('rating', 1.0))
    except ValueError:
        min_rating = 1.0

    query = {"rating": {"$gte": min_rating}}
    
    if selected_genres:
        genre_regex_list = [{"genre": {"$regex": genre, "$options": "i"}} for genre in selected_genres]
        query["$or"] = genre_regex_list

    matched_books = list(books_collection.find(query))
    matched_books = sorted(matched_books, key=lambda x: x.get('rating', 0), reverse=True)
    
    return render_template('results.html', books=matched_books, user_name=user_name)

if __name__ == '__main__':
    app.run(debug=True, port=5000)