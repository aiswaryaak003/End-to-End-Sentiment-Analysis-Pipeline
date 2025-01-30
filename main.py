from datasets import load_dataset
import sqlite3
import re
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

imdb_dataset = load_dataset("imdb")

conn = sqlite3.connect("imdb_reviews.db")

# Create a curser obj
cursor = conn.cursor()

# table created
cursor.execute("""
CREATE TABLE IF NOT EXISTS imdb_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto-incrementing ID
    review_text TEXT,
    sentiment TEXT
);
""")
conn.commit()

# Inserting data
for index, row in enumerate(imdb_dataset["train"]):
    cursor.execute(
    "INSERT INTO imdb_reviews (review_text, sentiment) VALUES (?, ?)", 
    (row["text"], "positive" if row["label"] == 1 else "negative")
    )

conn.commit()

conn.close()

# Function to clean text
def clean_text(text):
    text = text.lower() 
    text = re.sub(r"<br\s*/?>", " ", text) 
    text = re.sub(r"[^\w\s]", "", text)  
    return text

conn = sqlite3.connect("imdb_reviews.db")
cursor = conn.cursor()

df = pd.read_sql_query("SELECT * FROM imdb_reviews", conn)

df["cleaned_review"] = df["review_text"].apply(clean_text)

df["review_length"] = df["cleaned_review"].apply(lambda x: len(x.split()))

conn.close()

X_train, X_test, y_train, y_test = train_test_split(
    df["cleaned_review"], df["sentiment"], test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train LR model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

y_pred = model.predict(X_test_tfidf)

# Saving the model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

