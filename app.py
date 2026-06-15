import os
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'books.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

ALL_GENRES = ["Fantasy", "Adventure", "Mystery", "Thriller", "Science Fiction", "Romance", "Classic", "Drama", "Inspirational", "Self-Help", "Non-Fiction", "History"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", genres=ALL_GENRES)

@app.route("/recommend", methods=["POST"])
def recommend():
    preferred_genres = request.form.getlist("genres")
    user_name = request.form.get("user_name", "Reader").strip() or "Reader"
    
    raw_rating = request.form.get("min_rating")
    if raw_rating and raw_rating.strip():
        try:
            min_rating = float(raw_rating)
        except ValueError:
            min_rating = 3.0
    else:
        min_rating = 3.0

    conn = get_db_connection()
    
    if preferred_genres:
        placeholders = ', '.join('?' for _ in preferred_genres)
        query = f'SELECT * FROM books WHERE genre IN ({placeholders}) AND rating >= ?'
        params = preferred_genres + [min_rating]
        books = conn.execute(query, params).fetchall()
    else:
        books = conn.execute('SELECT * FROM books WHERE rating >= ?', (min_rating,)).fetchall()
        
    conn.close()
    return render_template("results.html", books=books, user_name=user_name)

@app.route("/all-books")
def all_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template("all_books.html", books=books)

if __name__ == "__main__":
    app.run(debug=True)