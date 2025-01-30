# Assignment-1
End-to-End Sentiment Analysis Pipeline

Overview:
This project implements an end-to-end sentiment analysis pipeline using Flask. It includes:
- Data collection, storage, and preprocessing
- Training a sentiment classifier
- Serving predictions via a REST API

Installation & Setup:

1. Clone the Repository:

git clone https://github.com/your-repo/sentiment-analysis-api.git
cd sentiment-analysis-api

2. Create a Virtual Environment (Recommended):

python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows

3. Install Dependencies:

pip install -r requirements.txt


4. Set Up MySQL Database:
   a) Install MySQL Server (if not already installed).
   b) Start MySQL and create the database:
   sql
   CREATE DATABASE sentiment_db;
   c) Create the required table:sql
   USE sentiment_db;
   CREATE TABLE imdb_reviews (
       id INT AUTO_INCREMENT PRIMARY KEY,
       review_text TEXT NOT NULL,
       sentiment VARCHAR(10) NOT NULL
   );

   d) Update the .env file with your MySQL credentials:

   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=yourpassword
   DB_NAME=sentiment_db
   ```

5. Run Database Migration (If Required):

python setup_db.py


Running the Flask API:
Start the Flask server:

python main.py

By default, it runs on http://127.0.0.1:5000

Testing the API:

1. Testing the /predict Endpoint:
Use Postman or cURL to send a POST request.

Example using Python (requests library):
python
import requests

url = "http://127.0.0.1:5000/predict"
data = {"review_text": "The movie was fantastic and thrilling!"}
response = requests.post(url, json=data)

print(response.json())  # Expected output: {"sentiment_prediction": "positive"}


2. Testing the Web Interface:
   a) Open http://127.0.0.1:5000 in your browser.
   b) Enter a review in the text box and click *Submit* to see the sentiment result.

Environment Variables:
Ensure the following environment variables are set (either in .env or directly in the terminal):

| Variable      | Description |
|--------------|-------------|
| DB_HOST    | Database hostname (default: localhost) |
| DB_USER    | MySQL username |
| DB_PASSWORD | MySQL password |
| DB_NAME    | Database name (sentiment_db) |

Deployment Notes:
For production deployment, use *Gunicorn* instead of Flask’s development server:

gunicorn -w 4 -b 0.0.0.0:5000 main:app
