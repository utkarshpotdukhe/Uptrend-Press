import os
import requests
from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime
import pytz  # For time zone support

# Load environment variables
load_dotenv()

# Flask app setup
app = Flask(__name__)

# Twitter API setup
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
BASE_URL = "https://api.twitter.com/2"

# Function to get user ID by username
def get_user_id(username):
    url = f"{BASE_URL}/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        return None

# Function to fetch tweets by user ID
def fetch_tweets(user_id):
    url = f"{BASE_URL}/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "tweet.fields": "created_at,public_metrics",  # Optional fields
        "max_results": 5  # Number of tweets to fetch
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        return []

# Flask routes
@app.route("/")
def index():
    # Twitter data fetching
    usernames = ["FlashStoX", "REDBOXINDIA"]  # Add more usernames here
    tweets_data = {}
    for username in usernames:
        user_id = get_user_id(username)
        if user_id:
            tweets = fetch_tweets(user_id)
            tweets_data[username] = tweets

    # Get current IST time
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

    return render_template("index.html", tweets_data=tweets_data, current_time=current_time)

if __name__ == "__main__":
    app.run(debug=True)
