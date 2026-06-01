import os
import pandas as pd
from googleapiclient.discovery import build
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load API key from .env file
load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

# Connect to YouTube API
youtube = build("youtube", "v3", developerKey=API_KEY)

# Search topics related to Dremel / DIY trends
SEARCH_TERMS = [
    "DIY woodworking UK",
    "furniture flip",
    "engraving projects",
    "cordless tool hacks",
    "DIY workshop setup"
]

all_videos = []

# Loop through each search term
for term in SEARCH_TERMS:

    print(f"\nSearching for: {term}")

    request = youtube.search().list(
        q=term,
        part="snippet",
        type="video",
        maxResults=10
    )

    response = request.execute()

    # Extract useful video information
    for item in response["items"]:

        video_data = {
            "search_term": term,
            "video_title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"],
            "description": item["snippet"]["description"]
        }

        all_videos.append(video_data)

# Convert to dataframe
df = pd.DataFrame(all_videos)

# Save to CSV
df.to_csv(BASE_DIR / "data" / "youtube_videos.csv", index=False)

# Display sample results
print("\nData Collection Complete.")
print(df.head())