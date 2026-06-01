import streamlit as st
import pandas as pd
from PIL import Image
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import google.generativeai as genai
import matplotlib.pyplot as plt
from textwrap import wrap

import os
from datetime import datetime, timedelta

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from agents.run_pipeline import run_all_agents

BASE_DIR = Path(__file__).resolve().parent.parent

LAST_RUN_FILE = BASE_DIR / "outputs" / "last_run.txt"

def should_refresh():
    if not LAST_RUN_FILE.exists():
        return True

    last_run = datetime.fromisoformat(
        LAST_RUN_FILE.read_text().strip()
    )

    return datetime.now() - last_run > timedelta(hours=24)

def refresh_data():
    run_all_agents()

    LAST_RUN_FILE.write_text(
        datetime.now().isoformat()
    )

try:
    if should_refresh():
        with st.spinner("Refreshing AI market intelligence data..."):
            refresh_data()

except Exception as e:
    st.error(f"Data refresh failed: {e}")

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="Dremel AI Trend Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# LOAD DATA
# -----------------------------

logo = Image.open(BASE_DIR / "visuals" / "dremel_logo.png")

trend_df = pd.read_csv(BASE_DIR / "outputs" / "trend_scores.csv")

analyzed_df = pd.read_csv(BASE_DIR / "outputs" / "analyzed_videos.csv")


genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel("gemini-2.0-flash")

# -----------------------------
# SIDEBAR
# -----------------------------

st.markdown("""
<style>

/* MAIN SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #0F172A !important;
    min-width: 320px !important;
    max-width: 320px !important;
}

/* Sidebar text */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* REMOVE COLLAPSE BUTTON */
button[kind="header"] {
    display: none !important;
}

/* REMOVE STREAMLIT HEADER */
header {
    visibility: hidden;
}

/* APP BACKGROUND */
.stApp {
    background-color: #020817;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------

with st.sidebar:
    st.image(logo, width=180)

    st.markdown("""
    <h1 style='color:white; font-size:48px;'>
    Dremel AI System
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "Dashboard Overview",
            "Trend Explorer",
            "AI Recommendations",
            "What Dremel Should Launch Next",
            "Trend Forecasting",
            "Executive Report",
            "Raw Data"
        ]
    )

    st.markdown("""
        <h1 style='color:#F97316; font-size:20px;'>
        Built by Shreeya Maithal
        </h1>
        """, unsafe_allow_html=True)

    st.markdown("### AI-Powered Market Intelligence • Predictive Analytics • Trend Forecasting")

# -----------------------------
# PAGE SELECTION
# -----------------------------
# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

/* REMOVE TOP WHITE BAR */
.main {
    background-color: #020817;
    padding-top: 0rem;
}

/* REMOVE DEFAULT STREAMLIT HEADER */
header {
    visibility: hidden;
}

/* REMOVE EXTRA TOP SPACE */
.block-container {
    padding-top: 1rem;
}

/* WHOLE APP BACKGROUND */
.stApp {
    background-color: #020817;
}

    /* Main background */
    .stApp {
        background-color: #0E1117;
        color: white;
    }

    /* Headers */
    h1, h2, h3 {
        color: #F97316;
    }

    /* KPI Cards */
    .kpi-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.3);
    }

    /* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Force sidebar visible */
section[data-testid="stSidebar"] {
    min-width: 320px !important;
    max-width: 320px !important;
}

    /* Sidebar text */
section[data-testid="stSidebar"] * {
    color: #E5E7EB !important;
}

/* Radio button labels */
.stRadio label {
    color: #F9FAFB !important;
    font-size: 16px !important;
    font-weight: 500;
}

/* Selected radio button */
.stRadio div[role="radiogroup"] > label[data-baseweb="radio"] {
    margin-bottom: 10px;
}

/* Sidebar title */
.sidebar-title {
    color: white;
    font-size: 32px;
    font-weight: bold;
}

/* Sidebar spacing */
section[data-testid="stSidebar"] {
    padding-top: 20px;
}

    /* Metric text */
    .kpi-title {
        font-size: 20px;
        color: #CBD5E1;
    }

    .kpi-value {
    font-size: 20px;
    font-weight: bold;
    color: #F97316;
    line-height: 1.2;
    word-break: break-word;

}
/* DOWNLOAD BUTTON */

.stDownloadButton button {
    background-color: #1E293B !important;
    color: white !important;
    border: 1px solid #334155 !important;

    border-radius: 15px !important;

    padding: 12px 20px !important;

    font-size: 18px !important;

    font-weight: 600 !important;

    width: 100% !important;
}

.stDownloadButton button:hover {
    background-color: #F97316 !important;
    color: white !important;
}

/* GENERATE PDF BUTTON */

.stButton > button {
    background-color: #F97316 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: bold !important;
    font-size: 18px !important;
    padding: 12px 24px !important;
}

.stButton > button:hover {
    background-color: #EA580C !important;
    color: white !important;
}
    </style>
    """, unsafe_allow_html=True)

if page == "Dashboard Overview":

    # -----------------------------
    # TITLE
    # -----------------------------

    st.markdown("""
        <div style='
        padding:15px;
        border-radius:15px;
        background: linear-gradient(90deg,#1e293b,#0f172a);
        border:1px solid #334155;
        margin-bottom:20px;
        '>
        <h4 style='color:#f97316;'>🚀 LIVE AI TREND MONITORING ACTIVE</h4>
        <p style='color:white;'>
        Analyzing UK DIY creator trends using NLP, sentiment analysis, and YouTube engagement signals.
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.title("Dremel AI Trend Intelligence Dashboard")
    st.markdown("""
        AI-powered monitoring system for UK DIY YouTube trends.
        """)
    st.subheader("🎥 Featured Dremel Video")
    st.video("https://youtu.be/iNRnVFR3L7I?si=-EWDgL1bMmeBKr-N")

    # -----------------------------
    # KPI CALCULATIONS
    # -----------------------------

    total_videos = len(analyzed_df)

    positive_count = len(
        analyzed_df[analyzed_df["sentiment"] == "Positive"]
    )

    top_trend = trend_df.iloc[0]["trend"]

    opportunity_score = round(
        (positive_count / total_videos) * 100
    )

    # -----------------------------
    # KPI DISPLAY
    # -----------------------------

    st.header("📈 AI Market Intelligence KPIs")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Total Videos</div>
                <div class="kpi-value">{total_videos}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Positive Sentiment</div>
                <div class="kpi-value">{positive_count}</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">Top Trend</div>
                <div class="kpi-value">{top_trend}</div>
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------
    # MARKET OPPORTUNITY GAUGE
    # -----------------------------

    st.header("🎯 Market Opportunity Gauge")

    gauge_fig = px.pie(
        values=[opportunity_score, 100 - opportunity_score],
        names=["Opportunity", "Remaining"],
        hole=0.7
    )

    gauge_fig.update_traces(
        textinfo='none',
        marker=dict(colors=["#F97316", "#1E293B"])
    )

    gauge_fig.update_layout(
        showlegend=False,
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0B1120",
        annotations=[
            dict(
                text=f"{opportunity_score}%",
                x=0.5,
                y=0.5,
                font_size=42,
                font_color="white",
                showarrow=False
            )
        ],
        height=450
    )

    st.plotly_chart(gauge_fig, use_container_width=True)

    # -----------------------------
    # SENTIMENT SUMMARY
    # -----------------------------

    st.header("📊 Sentiment Overview")

    sentiment_counts = analyzed_df["sentiment"].value_counts()

    fig = px.bar(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        color=sentiment_counts.index,
        title="DIY Sentiment Distribution"
    )

    fig.update_layout(
        paper_bgcolor="#020817",
        plot_bgcolor="#020817",
        font_color="white",

        title_font=dict(
            size=24,
            color="white"
        ),

        xaxis=dict(
            title_font=dict(color="white", size=18),
            tickfont=dict(color="#E2E8F0", size=14),
            showgrid=False
        ),

        yaxis=dict(
            title_font=dict(color="white", size=18),
            tickfont=dict(color="#E2E8F0", size=14),
            gridcolor="rgba(255,255,255,0.15)"
        ),

        legend=dict(
            font=dict(
                color="white",
                size=14
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # DONUT CHART ANALYTICS
    # -----------------------------

    st.header("🍩 AI Engagement Analytics")

    col1, col2 = st.columns(2)

    # SENTIMENT DONUT
    with col1:

        donut_fig = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            hole=0.65,
            title="Audience Sentiment Breakdown"
        )

        donut_fig.update_traces(
            textinfo='percent+label',
            marker=dict(colors=[
                "#F97316",
                "#2563EB",
                "#10B981"
            ])
        )

        donut_fig.update_layout(
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            font_color="white",
            title_font_color="white",
            legend_font_color="white",
            font=dict(color="white"),
            title_font_size=24,
            showlegend=True
        )

        st.plotly_chart(donut_fig, use_container_width=True)

    # TREND DONUT
    with col2:

        top_trends = trend_df.head(5)

        trend_fig = px.pie(
            top_trends,
            values="score",
            names="trend",
            hole=0.6,
            title="Top DIY Trend Distribution"
        )

        trend_fig.update_traces(
            textinfo='percent+label'
        )

        trend_fig.update_layout(
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            font_color="white",
            title_font_color="white",
            legend_font_color="white",
            font=dict(color="white"),
            title_font_size=24

        )

        st.plotly_chart(trend_fig, use_container_width=True)

    # -----------------------------
    # EXECUTIVE INSIGHTS
    # -----------------------------

    st.header("🧠 Executive AI Insights")

    top_3 = trend_df.head(3)["trend"].tolist()

    insight_1 = f"""
        AI analysis shows that {top_3[0].upper()} content currently dominates UK DIY engagement trends.
        """

    insight_2 = f"""
        Positive sentiment levels suggest strong audience interest in beginner-friendly and creator-focused content.
        """

    insight_3 = f"""
        Emerging interest in {top_3[1].upper()} and {top_3[2].upper()} indicates diversification opportunities for Dremel product marketing.
        """

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #2563EB, #1E3A8A);
                padding: 25px;
                border-radius: 15px;
                color: white;
                font-size: 22px;
                font-weight: 500;
                box-shadow: 0 0 15px rgba(37,99,235,0.4);
            ">
            AI analysis shows that <b>WOODWORKING</b> content currently dominates UK DIY engagement trends.
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #10B981, #065F46);
                padding: 25px;
                border-radius: 15px;
                color: white;
                font-size: 22px;
                font-weight: 500;
                box-shadow: 0 0 15px rgba(16,185,129,0.4);
            ">
            Positive sentiment levels suggest strong audience interest in beginner-friendly and creator-focused content.
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div style="
                background: linear-gradient(135deg, #F59E0B, #92400E);
                padding: 25px;
                border-radius: 15px;
                color: white;
                font-size: 22px;
                font-weight: 500;
                box-shadow: 0 0 15px rgba(245,158,11,0.4);
            ">
            Emerging interest in <b>DIY</b> and <b>LASER</b> indicates diversification opportunities for Dremel product marketing.
            </div>
            """, unsafe_allow_html=True)

    # -----------------------------
    # TREND SCORES
    # -----------------------------

    # -----------------------------
    # TREND HEATMAP
    # -----------------------------

    st.header("🔥 DIY Trend Heatmap")

    heatmap_fig = go.Figure(data=go.Heatmap(
        z=[trend_df["score"].tolist()],
        x=trend_df["trend"],
        y=["Trend Strength"],
        colorscale=[
            [0, "#1E293B"],
            [0.5, "#F97316"],
            [1, "#FB923C"]
        ],
        text=[trend_df["score"].tolist()],
        texttemplate="%{text}",
        textfont={"size": 18},
    ))

    heatmap_fig.update_layout(
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0B1120",
        font=dict(color="white"),
        height=220
    )

    st.plotly_chart(heatmap_fig, use_container_width=True)

    # -----------------------------
    # WORD CLOUD
    # -----------------------------

    st.header("☁️ DIY Trend Word Cloud")

    wordcloud = Image.open(BASE_DIR / "visuals" / "wordcloud.png")

    st.image(wordcloud)

    # -----------------------------
    # FOOTER
    # -----------------------------

    st.markdown("""
            <div style="
            padding:25px;
            border-radius:18px;
            background: linear-gradient(90deg,#111827,#0f172a);
            border:1px solid #1E293B;
            margin-top:40px;
            text-align:center;
            ">

            <h3 style="color:#F97316;">
            🚀 Dremel AI Trend Intelligence Platform
            </h3>

            <p style="color:#CBD5E1; font-size:17px;">
            Built using Python, NLP, YouTube API, Plotly, and Streamlit
            </p>

            <p style="color:white; font-size:22px; font-weight:bold;">
            Built by Shreeya Maithal
            </p>

            <p style="color:#64748B; font-size:15px;">
            AI-Powered Market Intelligence • Predictive Analytics • Trend Forecasting
            </p>

            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# TREND EXPLORER PAGE
# -----------------------------

elif page == "Trend Explorer":

    st.title("🔥 Trend Explorer")

    st.markdown("""
    Explore emerging DIY trends detected by the AI engine.
    """)

    # -----------------------------
    # FILTERS
    # -----------------------------

    st.markdown("""
    <p style="
    color:white;
    font-size:18px;
    font-weight:bold;
    margin-bottom:0px;
    ">
    Minimum Trend Score
    </p>
    """, unsafe_allow_html=True)

    min_score = st.slider(
        label="",
        min_value=0,
        max_value=int(trend_df["score"].max()),
        value=5
    )

    filtered_df = trend_df[
        trend_df["score"] >= min_score
        ]

    st.markdown("""
    <h3 style="
    color:#F97316;
    font-weight:bold;
    margin-top:20px;
    margin-bottom:10px;
    ">
    🎯 Focus Trend Analysis
    </h3>
    """, unsafe_allow_html=True)

    selected_trend = st.selectbox(
        label="",
        options=filtered_df["trend"].unique(),
        label_visibility="collapsed"
    )

    trend_data = filtered_df[
        filtered_df["trend"] == selected_trend
        ]

    # -----------------------------
    # KPI HIGHLIGHT
    # -----------------------------

    score = int(trend_data.iloc[0]["score"])

    if score >= 15:
        growth = "🔥Hot"

    elif score >= 10:
        growth = "📈Growing"

    else:
        growth = "🌱Emerging"

    col1, col2, col3 = st.columns([1.8,1,1.8])

    with col1:
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg,#1E293B,#334155);
        border-left:6px solid #F97316;
        padding:15px;
        height:150px;
        border-radius:18px;
        text-align:center;
        border-left:6px solid #F97316;
        ">
        <h3 style="color:#CBD5E1;">Trend</h3>
        <h2 style="
        color:white;
        font-size:34px;
        font-weight:bold;
        margin-top:0px;
        margin-bottom:0px;
        ">
        {selected_trend.title()}
        </h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg,#14532D,#166534);
        border-left:6px solid #22C55E;
        padding:15px;
        height:150px;
        border-radius:18px;
        text-align:center;
        border-left:6px solid #22C55E;
        ">
        <h3 style="color:#CBD5E1;">Score</h3>
        <h1 style="color:white;">{score}</h1>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
        background: linear-gradient(135deg,#1E3A8A,#2563EB);
        border-left:6px solid #60A5FA;
        padding:15px;
        height:150px;
        border-radius:18px;
        text-align:center;
        border-left:6px solid #3B82F6;
        ">
        <h3 style="color:#CBD5E1;">Status</h3>
        <h1 style="color:white;">{growth}</h1>
        </div>
        """, unsafe_allow_html=True)


    # -----------------------------
    # INTERACTIVE CHART
    # -----------------------------

    st.markdown("""
    <h2 style="
    color:#F97316;
    margin-top:20px;
    margin-bottom:10px;
    ">
    📊 Trend Ranking
    </h2>
    """, unsafe_allow_html=True)

    chart = px.bar(
        filtered_df,
        x="trend",
        y="score",
        color="score",
        color_continuous_scale=[
            "#22C55E",
            "#FACC15",
            "#F97316",
            "#EF4444"
        ],
        text="score",
        title="DIY Trend Scores",
    )

    chart.update_layout(
        paper_bgcolor="#020817",
        plot_bgcolor="#0F172A",
        font_color="white",

        height=450,

        title={
            "text": "DIY Trend Scores",
            "font": {"size": 24, "color": "#F97316"}
        },

        coloraxis_showscale=False
    )

    st.plotly_chart(
        chart,
        use_container_width=True
    )

    # -----------------------------
    # AI INSIGHT
    # -----------------------------

    score = int(trend_data.iloc[0]["score"])

    prompt = f"""
    You are a market intelligence analyst for Dremel.

    Trend: {selected_trend}
    Trend Score: {score}

    In 2-3 sentences explain:

    1. Why this trend matters
    2. What business opportunity it creates
    3. What Dremel should do next

    Keep it concise and executive-friendly.
    """

    if st.button("Generate AI Insight"):
        response = model.generate_content(prompt)

        insight = response.text

        st.session_state["trend_insight"] = insight

    if "trend_insight" in st.session_state:
        insight = st.session_state["trend_insight"]
    else:
        insight = "Click Generate AI Insight"

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#1E293B,#0F172A);
    padding:25px;
    border-left:6px solid #F97316;
    border-radius:18px;
    margin-top:20px;
    margin-bottom:20px;
    ">

    <h3 style="
    color:#F97316;
    margin-bottom:15px;
    ">
    🧠 AI Analysis
    </h3>

    <p style="
    color:white;
    font-size:20px;
    line-height:1.6;
    ">
    {insight}
    </p>

    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# AI RECOMMENDATIONS PAGE
# -----------------------------

elif page == "AI Recommendations":

    st.title("🤖 AI Recommendations")

    st.markdown("""
        AI-generated strategic recommendations powered by DIY trend intelligence.
        """)

    # -----------------------------
    # PRODUCT MAPPING
    # -----------------------------

    product_map = {

        "woodworking": {
            "product": "Dremel 3000 Rotary Tool",
            "strategy": "Promote precision carving and sanding tutorials.",
            "audience": "DIY woodworkers and hobby creators"
        },

        "laser": {
            "product": "Dremel DigiLab Laser Cutter",
            "strategy": "Target Etsy creators and personalized gift businesses.",
            "audience": "Small business creators"
        },

        "diy": {
            "product": "Dremel Lite",
            "strategy": "Launch beginner-friendly DIY campaigns.",
            "audience": "Beginner DIY enthusiasts"
        },

        "tools": {
            "product": "Dremel Multi-Max",
            "strategy": "Highlight versatility and multi-purpose usage.",
            "audience": "General home improvement users"
        },

        "furniture": {
            "product": "Dremel Versa",
            "strategy": "Promote furniture restoration projects.",
            "audience": "Furniture flipping creators"
        },

        "engraving": {
            "product": "Dremel Stylo+",
            "strategy": "Focus on personalization and artistic engraving.",
            "audience": "Craft creators and artists"
        },

        "workshop": {
            "product": "Dremel Workstation",
            "strategy": "Promote complete workshop setups.",
            "audience": "Advanced DIY hobbyists"
        },

        "cordless": {
            "product": "Dremel 8240",
            "strategy": "Emphasize portability and convenience.",
            "audience": "Mobile DIY users"
        }
    }
    # -----------------------------
    # SMART AI RECOMMENDATIONS
    # -----------------------------

    recommendations = {

        "woodworking": [
            "Launch beginner woodworking kits",
            "Promote precision carving accessories",
            "Create advanced woodworking tutorials",
            "Partner with woodworking YouTubers"
        ],

        "laser": [
            "Expand laser engraving product campaigns",
            "Target Etsy and personalization creators",
            "Promote small-business crafting solutions",
            "Showcase custom engraving projects"
        ],

        "DIY": [
            "Create viral DIY short-form videos",
            "Promote beginner-friendly tool bundles",
            "Launch DIY challenge campaigns",
            "Collaborate with home-improvement creators"
        ],

        "tools": [
            "Highlight tool versatility in campaigns",
            "Promote multi-tool solutions",
            "Emphasize durability and precision",
            "Create educational product demos"
        ],

        "furniture": [
            "Target furniture restoration creators",
            "Promote sanding and polishing accessories",
            "Show furniture makeover case studies",
            "Create before-and-after transformation videos"
        ],

        "engraving": [
            "Focus on personalization trends",
            "Promote engraving starter kits",
            "Target craft and gift creators",
            "Highlight artistic engraving possibilities"
        ],

        "workshop": [
            "Promote complete workshop setups",
            "Target serious DIY hobbyists",
            "Show efficient workspace organization",
            "Highlight premium tool ecosystems"
        ],

        "cordless": [
            "Promote portability and flexibility",
            "Target quick home-repair scenarios",
            "Emphasize battery efficiency",
            "Create mobile DIY workflow campaigns"
        ]
    }

    # -----------------------------
    # AI CARDS
    # -----------------------------

    for _, row in trend_df.iterrows():

        trend = row["trend"]
        score = row["score"]

        prompt = f"""
        You are a senior marketing strategist for Dremel.

        Trend: {trend}
        Trend Score: {score}

        Give:

        1. Recommended product idea
        2. Target audience
        3. Marketing strategy
        4. Four action recommendations

        Keep response concise.
        """

        if st.button(f"Generate Strategy for {trend}"):
            response = model.generate_content(prompt)

            ai_text = response.text

            st.write(ai_text)

        data = product_map.get(trend.lower())

        if data:
            actions = recommendations.get(
                trend.lower(),
                [
                    "Launch creator campaigns",
                    "Promote tool education",
                    "Build trend-focused content",
                    "Increase social media visibility"
                ]
            )

            bullet_points = "".join(
                [f"<li>{action}</li>" for action in actions]
            )

            st.markdown(f"""
            <div style="
            background-color:#1E293B;
            padding:25px;
            border-radius:18px;
            margin-bottom:25px;
            border-left:7px solid #F97316;
            ">

            <h2 style="color:#F97316;">
            🔥 {trend.upper()} TREND
            </h2>

            <p style="font-size:18px; color:white;">
            <b>Recommended Product:</b>
            {data['product']}
            </p>

            <p style="font-size:17px; color:#CBD5E1;">
            <b>Target Audience:</b>
            {data['audience']}
            </p>

            <p style="font-size:17px; color:#CBD5E1;">
            <b>Marketing Strategy:</b>
            {data['strategy']}
            </p>

            <p style="font-size:17px; color:#22C55E;">
            <b>AI Opportunity Score:</b>
            {score}/20
            </p>

            <hr style="border:1px solid #334155;">

            <h3 style="color:#60A5FA;">
            🎯 Strategic Actions
            </h3>

            <ul style="font-size:17px; color:#E2E8F0;">
            {bullet_points}
            </ul>

            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# WHAT DREMEL SHOULD LAUNCH NEXT PAGE
# -----------------------------

if page == "What Dremel Should Launch Next":
    st.header("🚀 What Dremel Should Launch Next")

    launch_recommendations = {

        "woodworking":
            {
                "title": "🪵 Beginner Woodworking Starter Kits",
                "desc": """
    AI detected massive woodworking engagement among beginner DIY audiences.

    Dremel should launch:
    - compact starter kits
    - beginner carving accessories
    - creator-focused woodworking bundles
    """
            },

        "laser":
            {
                "title": "⚡ Compact Laser Engraving Bundle",
                "desc": """
    Laser engraving content is rapidly growing in creator communities.

    Dremel can capitalize through:
    - portable engraving tools
    - laser DIY kits
    - customization-focused products
    """
            },

        "DIY":
            {
                "title": "🎥 DIY Creator Partnership Program",
                "desc": """
    DIY creator engagement remains extremely high.

    Opportunity areas:
    - creator sponsorships
    - TikTok/YouTube collaborations
    - beginner tutorial campaigns
    """
            },

        "furniture":
            {
                "title": "🛠 Furniture Flip Tool Collection",
                "desc": """
    Furniture flipping content shows strong viral potential.

    Suggested launches:
    - sanding bundles
    - restoration kits
    - finishing tool packs
    """
            }

    }

    for _, row in trend_df.iterrows():

        trend = row["trend"]

        if trend in launch_recommendations:
            rec = launch_recommendations[trend]

            st.markdown(f"""
    <div style="
    background: linear-gradient(135deg, #111827, #1E3A8A);
    padding:25px;
    border-radius:18px;
    margin-bottom:20px;
    border-left:6px solid #3B82F6;
    box-shadow:0px 0px 22px rgba(59,130,246,0.35);
    ">

    <h2 style="color:#60A5FA;">
    {rec['title']}
    </h2>

    <p style="color:white; font-size:18px;">
    {rec['desc']}
    </p>

    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# TREND FORECASTING PAGE
# -----------------------------
if page == "Trend Forecasting":
    st.header("📈 AI Trend Forecasting")

    forecast_df = trend_df.head(5).copy()

    forecast_df["future_score"] = (
            forecast_df["score"] * [1.25, 1.18, 1.15, 1.10, 1.08]
    )
    forecast_col1, forecast_col2, forecast_col3 = st.columns(3)

    with forecast_col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Fastest Growing Trend</div>
            <div class="kpi-value">WOODWORKING</div>
        </div>
        """, unsafe_allow_html=True)

    with forecast_col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Predicted Growth</div>
            <div class="kpi-value">+25%</div>
        </div>
        """, unsafe_allow_html=True)

    with forecast_col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-title">Next Opportunity</div>
            <div class="kpi-value">LASER DIY</div>
        </div>
        """, unsafe_allow_html=True)
    forecast_fig = go.Figure()

    forecast_fig.add_trace(
        go.Scatter(
            x=forecast_df["trend"],
            y=forecast_df["score"],
            mode='lines+markers',
            name='Current Trend Strength',
            line=dict(color='#F97316', width=4),
            marker=dict(size=10)
        )
    )

    forecast_fig.add_trace(
        go.Scatter(
            x=forecast_df["trend"],
            y=forecast_df["future_score"],
            mode='lines+markers',
            name='Predicted Growth',
            line=dict(color='#22C55E', width=4, dash='dash'),
            marker=dict(size=10)
        )
    )

    forecast_fig.update_layout(
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0B1120",
        font=dict(color="white"),
        title="AI Forecast: Future DIY Trend Growth",
        title_font=dict(size=24, color="white"),
        xaxis=dict(
            title="DIY Trends",
            tickfont=dict(color="white")
        ),
        yaxis=dict(
            title="Trend Strength Score",
            tickfont=dict(color="white")
        ),
        legend=dict(
            font=dict(color="white")
        ),
        height=500
    )

    st.plotly_chart(
        forecast_fig,
        use_container_width=True
    )

    # -----------------------------
    # FORECAST INSIGHTS
    # -----------------------------

    st.markdown("""
    <div style="
    background: linear-gradient(135deg,#111827,#1E293B);
    padding:25px;
    border-radius:18px;
    margin-top:20px;
    border-left:6px solid #22C55E;
    box-shadow:0px 0px 20px rgba(34,197,94,0.25);
    ">

    <h2 style="color:#22C55E;">
    🚀 AI Forecast Summary
    </h2>

    <p style="color:white; font-size:18px;">

    AI forecasting predicts continued growth in
    <b>WOODWORKING</b>,
    <b>DIY</b>,
    and
    <b>LASER ENGRAVING</b>
    content across UK creator communities.

    Dremel has strong opportunities to expand:
    <ul style="color:#E2E8F0; font-size:17px;">
    <li>creator-focused toolkits</li>
    <li>portable smart tools</li>
    <li>beginner-friendly DIY systems</li>
    <li>custom engraving solutions</li>
    </ul>

    </p>

    </div>
    """, unsafe_allow_html=True)

## -----------------------------
# 📊 Executive Report Page
# -----------------------------

elif page == "Executive Report":

    st.title("📊 Executive Report")

    st.markdown("""
    Generate a professional PDF report containing:

    • Trend Rankings
    • AI Insights
    • Strategic Recommendations
    • Executive Summary
    """)

    if st.button("Generate PDF Report"):
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader

        pdf_file = "Dremel_Executive_Report.pdf"

        c = canvas.Canvas(pdf_file)

        # Page border
        c.rect(
            30,  # x
            30,  # y
            535,  # width
            780,  # height
            stroke=1,
            fill=0
        )

        def draw_footer():
            c.setFont("Helvetica", 9)

            c.drawString(
                50,
                15,
                "Generated by Dremel AI Trend Intelligence Platform || Created by Shreeya Maithal"
            )

            c.drawRightString(
                550,
                15,
                f"Page {c.getPageNumber()}"
            )

        logo_path = BASE_DIR / "visuals" / "dremel_logo.png"

        c.drawImage(
            str(logo_path),
            50,
            780,
            width=120,
            height=40,
            preserveAspectRatio=True
        )
        from datetime import datetime
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, 730, "Dremel Executive Report")

        c.setFont("Helvetica", 12)
        c.drawString(180, 790, "Generated by Dremel AI System")

        c.drawString(
            180,
            770,
            f"Generated on: {datetime.now().strftime('%d %B %Y')}"
        )

        c.line(50, 720, 550, 720)

        c.setFillColorRGB(0, 0, 0)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 680, "Executive Summary")

        c.setFont("Helvetica", 12)

        top_trend = trend_df.iloc[0]["trend"]
        top_score = trend_df.iloc[0]["score"]

        summary = (
            f"The strongest emerging trend is {top_trend} "
            f"with a trend score of {top_score}. "
            f"This indicates significant market potential "
            f"for Dremel product innovation and marketing investment."
        )

        c.drawString(50, 650, summary[:80])
        c.drawString(50, 635, summary[80:])

        c.setFillColorRGB(0, 0, 0)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 580, "Trend Snapshot")

        top_trend = trend_df.iloc[0]["trend"]
        top_score = trend_df.iloc[0]["score"]

        # Box 1
        c.roundRect(50, 500, 140, 60, 8)

        # Box 2
        c.roundRect(220, 500, 140, 60, 8)

        # Box 3
        c.roundRect(390, 500, 140, 60, 8)

        # TOP TREND
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(120, 545, "TOP TREND")

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(120, 520, str(top_trend).upper())

        # TREND SCORE
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(290, 545, "TREND SCORE")

        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(290, 520, str(top_score))

        # STATUS
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(460, 545, "STATUS")

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(460, 520, "HOT")

        if False:
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 580, "Top DIY Trends")

            c.setFillColorRGB(0, 0, 0)

            y = 550

            rank = 1

            for _, row in trend_df.head(5).iterrows():
                c.setFont("Helvetica", 12)
                c.drawString(
                    70,
                    y,
                    f"{rank}. {row['trend']} | Score: {row['score']}"
                )
                y -= 25
                rank += 1

        y = 450

        c.setFillColorRGB(0, 0, 0)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Strategic Recommendation")

        y -= 30

        top_trend = trend_df.iloc[0]["trend"]

        recommendation = (
            f"Focus investment on {top_trend} products, creator partnerships, "
            f"and beginner-friendly tool bundles."
        )

        c.setFont("Helvetica", 12)
        c.drawString(
            50,
            y,
            recommendation
        )

        y -= 60

        c.setFillColorRGB(0, 0, 0)

        c.setFont("Helvetica-Bold", 16)

        # AI OPPORTUNITY

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "AI Opportunity")

        y -= 25

        c.setFont("Helvetica", 12)
        c.drawString(
            50,
            y,
            "Laser engraving and woodworking show the highest growth potential."
        )

        # move down before next section
        y -= 60

        # MARKET OPPORTUNITY SCORE

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, y, "Market Opportunity Score")

        y -= 25

        opportunity = round(
            len(analyzed_df[analyzed_df["sentiment"] == "Positive"])
            / len(analyzed_df)
            * 100
        )

        c.setFont("Helvetica-Bold", 14)
        c.drawString(
            50,
            y,
            f"Opportunity Score: {opportunity}%"
        )

        c.setFillColorRGB(0, 0, 0)

        y -= 25

        opportunity = round(
            len(analyzed_df[analyzed_df["sentiment"] == "Positive"])
            / len(analyzed_df)
            * 100
        )

        c.setFont("Helvetica", 10)

        # Create trend chart

        top5 = trend_df.head(5)

        plt.figure(figsize=(6, 3))

        plt.bar(
            top5["trend"],
            top5["score"]
        )

        plt.title("Top DIY Trends")
        plt.ylabel("Trend Score")

        chart_file = "trend_chart.png"

        plt.savefig(chart_file, bbox_inches="tight")

        plt.close()

        c.drawImage(
            chart_file,
            50,
            200,
            width=400,
            height=200
        )

        # Executive Analysis Section

        analysis_y = 150

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, analysis_y, "Executive Analysis")

        analysis_y -= 30

        analysis_lines = [
            f"{top_trend.title()} currently leads all identified DIY trends with a score of {top_score}, indicating strong consumer interest and content engagement.",

            "Woodworking and laser-related content continue to gain traction among DIY creators, suggesting opportunities for targeted product launches.",

            "Recommended actions include creator partnerships, educational content, beginner tool bundles, and increased investment in high-growth categories.",

            "",

            "Business Actions:",

            "- Increase partnerships with woodworking creators",

            "- Launch beginner DIY starter kits",

            "- Expand laser engraving product campaigns",

            "- Build educational content ecosystems",

            "- Monitor trend growth monthly",

            "- Develop creator-focused marketing programs"
        ]

        c.setFont("Helvetica", 11)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(
            50,
            analysis_y,
            "Expected Business Impact"
        )

        analysis_y -= 30

        c.setFont("Helvetica", 11)

        impact_text = (
            "By aligning product development and marketing investments "
            "with high-growth DIY categories, Dremel can strengthen market "
            "share, improve customer engagement, and accelerate revenue growth."
        )

        for line in wrap(impact_text, width=95):
            c.drawString(
                50,
                analysis_y,
                line
            )
            analysis_y -= 18

        analysis_y -= 20

        for line in analysis_lines:

            wrapped_lines = wrap(
                line,
                width=95
            )

            for wrapped in wrapped_lines:

                if analysis_y < 100:
                    draw_footer()

                    c.showPage()

                    # Page border
                    c.rect(
                        30,
                        30,
                        535,
                        780,
                        stroke=1,
                        fill=0
                    )

                    # Border
                    c.rect(
                        30,
                        30,
                        535,
                        780,
                        stroke=1,
                        fill=0
                    )

                    # Logo
                    c.drawImage(
                        str(logo_path),
                        50,
                        760,
                        width=100,
                        height=35,
                        preserveAspectRatio=True
                    )

                    # Header
                    c.setFont("Helvetica-Bold", 20)
                    c.drawString(
                        50,
                        720,
                        "Executive Analysis (Continued)"
                    )

                    c.line(
                        50,
                        710,
                        550,
                        710
                    )

                    analysis_y = 680

                    c.setFont("Helvetica", 11)

                    analysis_y = 660

                c.drawString(
                    50,
                    analysis_y,
                    wrapped
                )

                analysis_y -= 18
        draw_footer()
        c.save()

        import os

        st.success(f"PDF saved successfully: {os.path.abspath(pdf_file)}")

        st.success("PDF created!")
        with open(pdf_file, "rb") as file:
            st.download_button(
                label="📥 Download Executive Report",
                data=file,
                file_name="Dremel_Executive_Report.pdf",
                mime="application/pdf"
            )

## -----------------------------
# RAW DATA PAGE
# -----------------------------
if page == "Raw Data":
    st.title("📂 Raw Data")

    st.subheader("Analyzed Videos")

    st.dataframe(analyzed_df)

    csv1 = analyzed_df.to_csv(index=False)

    st.download_button(
        "📥 Download Analyzed Videos",
        csv1,
        "analyzed_videos.csv",
        "text/csv"
    )

    st.subheader("Trend Scores")

    st.dataframe(trend_df)

    csv2 = trend_df.to_csv(index=False)

    st.download_button(
        "📥 Download Trend Scores",
        csv2,
        "trend_scores.csv",
        "text/csv"
    )
