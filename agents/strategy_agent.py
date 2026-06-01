import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Load analyzed data
df = pd.read_csv(BASE_DIR / "outputs" / "analyzed_videos.csv")

# -----------------------------
# TREND SCORING
# -----------------------------

# Count keyword frequency
all_text = " ".join(df["clean_text"].astype(str))

keywords = [
    "woodworking",
    "engraving",
    "furniture",
    "workshop",
    "tools",
    "diy",
    "laser",
    "cordless"
]

trend_scores = {}

for keyword in keywords:

    count = all_text.count(keyword)

    trend_scores[keyword] = count

# Convert to dataframe
trend_df = pd.DataFrame(
    trend_scores.items(),
    columns=["trend", "score"]
)

# Sort trends
trend_df = trend_df.sort_values(
    by="score",
    ascending=False
)

# -----------------------------
# AI STRATEGIC RECOMMENDATIONS
# -----------------------------

recommendations = []

for _, row in trend_df.iterrows():

    trend = row["trend"]
    score = row["score"]

    if score >= 5:

        recommendation = f"""
TREND DETECTED: {trend.upper()}

WHY IT MATTERS:
High visibility in UK DIY content ecosystem.

DREMEL SHOULD:
- Create short-form content around {trend}
- Collaborate with DIY creators
- Build tutorial-based campaigns
- Promote beginner-friendly tools
"""

        recommendations.append(recommendation)

# -----------------------------
# OUTPUT RESULTS
# -----------------------------

print("\n========== TREND SCORES ==========")
print(trend_df)

print("\n========== STRATEGIC RECOMMENDATIONS ==========")

for rec in recommendations:
    print(rec)

# Save trend report
trend_df.to_csv(BASE_DIR / "outputs" / "trend_scores.csv", index=False)

print("\nStrategy Agent Complete.")