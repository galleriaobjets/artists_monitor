import streamlit as st
import pandas as pd
from datetime import datetime

# Dummy scraper function — replace with real logic later
def scrape_artrabbit():
    return [
        {
            "artist_or_title": "Alice Romano",
            "region": "UK",
            "event_url": "https://example.com/event1",
            "source": "ArtRabbit",
            "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        },
        {
            "artist_or_title": "Marco Neri",
            "region": "Italy",
            "event_url": "https://example.com/event2",
            "source": "ArtRabbit",
            "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
    ]

# App layout
st.set_page_config(page_title="Artist Momentum Tracker", layout="wide")
st.title("🎨 Emerging Artist Momentum Tracker")

# Sidebar controls
st.sidebar.header("🛠 Run Scrapers")

if st.sidebar.button("Run ArtRabbit Scraper"):
    scraped_data = scrape_artrabbit()
    df = pd.DataFrame(scraped_data)
    df.to_csv("artist_list.csv", index=False)
    st.success(f"{len(df)} new artist records saved.")
    st.dataframe(df)
else:
    try:
        df = pd.read_csv("artist_list.csv")
        st.subheader("📋 Tracked Artists")
        st.dataframe(df)
    except FileNotFoundError:
        st.warning("No data available yet. Run a scraper to get started.")

# Future layout for analytics
st.markdown("---")
st.header("📈 Momentum Scores, Mentions, and Trends (coming soon)")
st.info("This section will display data visualizations and momentum scoring.")
