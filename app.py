from flask import Flask, request, render_template 
import pickle
import re

# Load the saved model and vectorizer
with open(r"C:\Users\USER\Desktop\cogninest ai\model.pkl", "rb") as f:
    loaded_model = pickle.load(f)
with open(r"C:\Users\USER\Desktop\cogninest ai\vectorizer.pkl", "rb") as f:
    loaded_vectorizer = pickle.load(f)

# Initialize Flask app
app = Flask(__name__,template_folder=r"C:\Users\USER\Desktop\cogninest ai\cogai\templates")

# Load the trained model and vectorizer
with open(r'C:\Users\USER\Desktop\cogninest ai\model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open(r'C:\Users\USER\Desktop\cogninest ai\vectorizer.pkl', 'rb') as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Preprocessing function
def preprocess_text(text):
    text = text.lower()  # Convert to lowercase
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text

@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = None  # Variable to hold the sentiment prediction

    if request.method == "POST":
        # Get the input review text from the form
        review_text = request.form.get("review_text")

        if review_text:
            # Preprocess the text
            cleaned_text = preprocess_text(review_text)

            # Convert to TF-IDF vector
            text_vector = vectorizer.transform([cleaned_text])

            # Predict sentiment
            prediction = model.predict(text_vector)
            print("Model Prediction Output:", prediction)

            # Map numeric prediction to sentiment labels
            sentiment = "Positive" if prediction[0].lower() == 'positive' else "Negative"

    print("Sentiment (Before Rendering):", sentiment)

    return render_template("index.html", sentiment=sentiment)

if __name__ == "__main__":
    app.run(debug=True)
