import os
from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# ─── MongoDB Connection ────────────────────────────────────────────────────────
# Use environment variables for MongoDB Atlas
#   set MONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/book_recommender
#   set MONGO_DB=book_recommender
mongo_uri = os.environ.get("MONGO_URI")
mongo_db_name = os.environ.get("MONGO_DB", "BOOKMind")
use_mongo = True
sample_books = [
    {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling",
     "genres": ["Fantasy", "Adventure"], "rating": 4.8,
     "description": "A young wizard discovers his magical heritage.", "cover_color": "#7B2D8B"},
    {"title": "The Hobbit", "author": "J.R.R. Tolkien",
     "genres": ["Fantasy", "Adventure"], "rating": 4.7,
     "description": "Bilbo Baggins embarks on an unexpected journey.", "cover_color": "#2E7D32"},
    {"title": "The Da Vinci Code", "author": "Dan Brown",
     "genres": ["Mystery", "Thriller"], "rating": 4.3,
     "description": "A Harvard professor unravels a religious mystery.", "cover_color": "#1565C0"},
    {"title": "Gone Girl", "author": "Gillian Flynn",
     "genres": ["Mystery", "Thriller"], "rating": 4.0,
     "description": "A husband becomes the prime suspect in his wife's disappearance.", "cover_color": "#B71C1C"},
    {"title": "Dune", "author": "Frank Herbert",
     "genres": ["Science Fiction", "Adventure"], "rating": 4.6,
     "description": "A noble family controls the desert planet Arrakis.", "cover_color": "#E65100"},
    {"title": "The Martian", "author": "Andy Weir",
     "genres": ["Science Fiction"], "rating": 4.5,
     "description": "An astronaut must survive alone on Mars.", "cover_color": "#D84315"},
    {"title": "Pride and Prejudice", "author": "Jane Austen",
     "genres": ["Romance", "Classic"], "rating": 4.6,
     "description": "Elizabeth Bennet navigates love and social class.", "cover_color": "#880E4F"},
    {"title": "The Notebook", "author": "Nicholas Sparks",
     "genres": ["Romance"], "rating": 4.1,
     "description": "A timeless love story spanning decades.", "cover_color": "#AD1457"},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee",
     "genres": ["Classic", "Drama"], "rating": 4.8,
     "description": "A lawyer defends a Black man in the American South.", "cover_color": "#4A148C"},
    {"title": "1984", "author": "George Orwell",
     "genres": ["Science Fiction", "Classic"], "rating": 4.7,
     "description": "A dystopian society under constant government surveillance.", "cover_color": "#263238"},
    {"title": "The Alchemist", "author": "Paulo Coelho",
     "genres": ["Adventure", "Inspirational"], "rating": 4.3,
     "description": "A shepherd boy travels in search of treasure.", "cover_color": "#F57F17"},
    {"title": "Atomic Habits", "author": "James Clear",
     "genres": ["Self-Help", "Inspirational"], "rating": 4.8,
     "description": "Tiny changes that lead to remarkable results.", "cover_color": "#00838F"},
    {"title": "Sherlock Holmes", "author": "Arthur Conan Doyle",
     "genres": ["Mystery", "Classic"], "rating": 4.7,
     "description": "The world's greatest detective solves impossible cases.", "cover_color": "#37474F"},
    {"title": "The Hunger Games", "author": "Suzanne Collins",
     "genres": ["Science Fiction", "Adventure", "Thriller"], "rating": 4.5,
     "description": "Teens fight to the death in a dystopian society.", "cover_color": "#BF360C"},
    {"title": "Sapiens", "author": "Yuval Noah Harari",
     "genres": ["Non-Fiction", "History"], "rating": 4.4,
     "description": "A brief history of humankind.", "cover_color": "#1A237E"},
]

try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[mongo_db_name]
    books_collection = db["books"]
except Exception as exc:
    print(f"⚠️ MongoDB connection failed: {exc}")
    print("Using in-memory sample books instead.")
    books_collection = None
    use_mongo = False

# ─── Seed sample books if DB is empty ─────────────────────────────────────────
def get_all_books():
    if use_mongo and books_collection is not None:
        return list(books_collection.find({}, {"_id": 0}))
    return [book.copy() for book in sample_books]


def seed_books():
    if not use_mongo or books_collection is None:
        return

    if books_collection.count_documents({}) == 0:
        books_collection.insert_many(sample_books)
        print("✅ Sample books inserted into MongoDB.")

# ─── AI Recommendation Engine ─────────────────────────────────────────────────
def calculate_match_score(book, preferred_genres, min_rating):
    """
    Match Score Formula (from project spec):
    Score = (Genre Overlap × 50) + (Rating × 50)
    """
    book_genres = set(book.get("genres", []))
    user_genres = set(preferred_genres)

    # Genre overlap ratio (0.0 to 1.0)
    if len(user_genres) == 0:
        genre_overlap = 0
    else:
        overlap_count = len(book_genres & user_genres)
        genre_overlap = overlap_count / len(user_genres)

    # Rating normalised to 0.0–1.0 scale (max rating = 5.0)
    rating = book.get("rating", 0)
    normalised_rating = rating / 5.0

    # Final score (0–100)
    score = (genre_overlap * 50) + (normalised_rating * 50)
    return round(score, 1)

def get_recommendations(preferred_genres, min_rating):
    all_books = get_all_books()

    # Step 1 – Calculate match score for every book
    for book in all_books:
        book["match_score"] = calculate_match_score(book, preferred_genres, min_rating)

    # Step 2 – Rank by match score descending
    ranked = sorted(all_books, key=lambda x: x["match_score"], reverse=True)

    # Step 3 – Filter out books below 40 % match AND below min rating
    if preferred_genres:
        # If genres were selected, ensure at least one genre matches using set intersection
        top_picks = [
            b for b in ranked 
            if b["match_score"] >= 40 
            and b["rating"] >= min_rating 
            and set(b["genres"]) & set(preferred_genres)
        ]
    else:
        # If no genres were selected, just filter by score and rating
        top_picks = [b for b in ranked if b["match_score"] >= 40 and b["rating"] >= min_rating]

    return top_picks
# ─── Routes ───────────────────────────────────────────────────────────────────
ALL_GENRES = ["Fantasy", "Adventure", "Mystery", "Thriller",
              "Science Fiction", "Romance", "Classic",
              "Drama", "Inspirational", "Self-Help", "Non-Fiction", "History"]

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", genres=ALL_GENRES)

@app.route("/recommend", methods=["POST"])
def recommend():
    preferred_genres = request.form.getlist("genres")   # multi-select checkboxes
    min_rating       = float(request.form.get("min_rating", 3.0))
    user_name        = request.form.get("user_name", "Reader").strip() or "Reader"

    recommendations  = get_recommendations(preferred_genres, min_rating)

    return render_template(
        "results.html",
        books=recommendations,
        genres=preferred_genres,
        min_rating=min_rating,
        user_name=user_name,
        all_genres=ALL_GENRES,
    )

@app.route("/all-books")
def all_books():
    books = get_all_books()
    return render_template("all_books.html", books=books)

# ─── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    seed_books()
    app.run(debug=True)
