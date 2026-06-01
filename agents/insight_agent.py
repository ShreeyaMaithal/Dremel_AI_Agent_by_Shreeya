import pandas as pd
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Load collected YouTube data
df = pd.read_csv(BASE_DIR / "data" / "youtube_videos.csv")

# Combine title + description
df["combined_text"] = (
    df["video_title"].astype(str) + " " +
    df["description"].astype(str)
)

# Clean text function
def clean_text(text):

    # Convert everything to string
    text = str(text)

    # Lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\\S+", "", text)

    # Remove special characters
    text = re.sub(r"[^a-zA-Z ]", "", text)

    return text

# Apply cleaning
df["clean_text"] = df["combined_text"].apply(clean_text)

# -----------------------------
# SENTIMENT ANALYSIS
# -----------------------------

analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):

    score = analyzer.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive"

    elif score <= -0.05:
        return "Negative"

    else:
        return "Neutral"

df["sentiment"] = df["clean_text"].apply(get_sentiment)

# -----------------------------
# KEYWORD EXTRACTION
# -----------------------------

vectorizer = CountVectorizer(
    stop_words="english",
    max_features=20
)
X = vectorizer.fit_transform(df["clean_text"])
df = df[df["clean_text"] != "nan"]

X = vectorizer.fit_transform(df["clean_text"])

keywords = vectorizer.get_feature_names_out()

# -----------------------------
# RESULTS
# -----------------------------

print("\n========== SENTIMENT COUNTS ==========")
print(df["sentiment"].value_counts())

print("\n========== TOP KEYWORDS ==========")
print(keywords)

# Save processed results
df.to_csv(BASE_DIR / "outputs" / "analyzed_videos.csv", index=False)

print("\nInsight Agent Analysis Complete.")