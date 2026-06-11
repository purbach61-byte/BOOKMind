# 📚 BookMind – AI Book Recommendation System

An AI-powered book recommender built as a mini project using:
**Python · Flask · MongoDB · PyMongo · Bootstrap 5 · Jinja2 · HTML/CSS**

---

## 🚀 How to Run

### Step 1 – Install MongoDB
Download and install MongoDB Community Edition from https://www.mongodb.com/try/download/community
Start the MongoDB service before running the app.

### Step 2 – Install Python dependencies
Open a terminal in the project folder and run:
```
pip install -r requirements.txt
```

### Step 3 – Run the Flask app
```
python app.py
```

### Step 4 – Open in browser
Visit: http://127.0.0.1:5000

The app will automatically seed 15 sample books into MongoDB on first run.

---

## 🧠 AI Inference Engine

The recommendation algorithm works in 4 steps:

1. **User inputs** preferred genres + minimum rating
2. **Match Score** calculated for every book:
   ```
   Score = (Genre Overlap × 50) + (Normalised Rating × 50)
   ```
   - Genre Overlap = (matching genres) ÷ (total user genres)  → 0.0–1.0
   - Normalised Rating = book rating ÷ 5.0  → 0.0–1.0
3. **Ranked** by score descending
4. **Filtered** – books with < 40% match score are removed

---

## 📁 Project Structure

```
book_recommender/
│
├── app.py                  ← Flask app + AI engine
├── requirements.txt        ← Python dependencies
│
├── templates/
│   ├── base.html           ← Navbar + footer layout
│   ├── index.html          ← Home page with preference form
│   ├── results.html        ← Book recommendation cards
│   └── all_books.html      ← Full library table
│
└── static/
    ├── css/style.css       ← Custom dark-theme stylesheet
    └── js/main.js          ← Slider + animation JS
```

---

## 💻 Technology Stack

| Technology | Purpose |
|------------|---------|
| HTML       | Frontend structure and form layout |
| CSS        | Styling, card layout, responsive design |
| Bootstrap 5| Responsive UI components |
| Python     | Backend logic and inference engine |
| Flask      | Web framework and routing |
| MongoDB    | NoSQL database for book inventory |
| PyMongo    | Python driver for MongoDB queries |
| Jinja2     | Dynamic template rendering for results |
