import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Bearer Token from environment variables
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Base URL for Twitter API
BASE_URL = "https://api.twitter.com/2"

# Function to get user ID by username
def get_user_id(username):
    url = f"{BASE_URL}/users/by/username/{username}"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["id"]
    else:
        print(f"Error fetching user ID for {username}: {response.status_code} - {response.json()}")
        return None

# Function to fetch tweets by user ID
def fetch_tweets(user_id):
    url = f"{BASE_URL}/users/{user_id}/tweets"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "tweet.fields": "created_at,public_metrics",  # Optional fields
        "max_results": 5  # Number of tweets to fetch (max 100)
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching tweets for user ID {user_id}: {response.status_code} - {response.json()}")
        return None

# Main function to fetch tweets for multiple users
def main():
    usernames = ["FlashStoX", "REDBOXINDIA"]  # Add more usernames as needed
    for username in usernames:
        print(f"Fetching tweets for: {username}")
        user_id = get_user_id(username)
        if user_id:
            tweets = fetch_tweets(user_id)
            if tweets:
                print(f"Tweets for {username}:")
                for tweet in tweets:
                    print(f"- {tweet['created_at']}: {tweet['text']}")
                print("\n")
            else:
                print(f"No tweets found for {username}.")
        else:
            print(f"Unable to fetch data for {username}.")

# Run the main function
if __name__ == "__main__":
    main()
