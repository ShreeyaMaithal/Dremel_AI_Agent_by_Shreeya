import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load analyzed data
df = pd.read_csv(BASE_DIR / "outputs" / "analyzed_videos.csv")

# -----------------------------
# SENTIMENT VISUALIZATION
# -----------------------------

sentiment_counts = df["sentiment"].value_counts()

plt.figure(figsize=(6, 4))

sentiment_counts.plot(kind="bar")

plt.title("DIY YouTube Sentiment Analysis")
plt.xlabel("Sentiment")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(BASE_DIR / "visuals" / "sentiment_chart.png")

print("Sentiment chart saved.")

# -----------------------------
# WORD CLOUD
# -----------------------------

all_words = " ".join(df["clean_text"].astype(str))

wordcloud = WordCloud(
    width=1000,
    height=500,
    background_color="white"
).generate(all_words)

plt.figure(figsize=(10, 5))

plt.imshow(wordcloud, interpolation="bilinear")

plt.axis("off")

plt.tight_layout()

plt.savefig(BASE_DIR / "visuals" / "wordcloud.png")

print("Word cloud saved.")

print("\nReport Agent Complete.")