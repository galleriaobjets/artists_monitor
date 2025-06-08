# streamlit_app.py

import streamlit as st
import pandas as pd
from scraper_suite import scrape_artrabbit, scrape_artsy_editorial, scrape_frieze_articles, scrape_google_news
from instagram_and_gallery_scrapers import scrape_instagram_hashtag_preview, scrape_all_galleries
from datetime import datetime
import os

# ---------- Config ----------
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ---------- Page Setup ----------
st.set_page_config(page_title="Artist Momentum Tracker", layout="wide")
st.title("🎨 Emerging Artist Momentum Tracker")
st.sidebar.header("🛠 Run Data Collection")

# ---------- Button Controls ----------
if st.sidebar.button("Scrape ArtRabbit"):
    df = scrape_artrabbit()
    df.to_csv(f"{DATA_FOLDER}/artrabbit.csv", index=False)
    st.success(f"Scraped {len(df)} records from ArtRabbit.")
    st.dataframe(df)

if st.sidebar.button("Scrape Artsy Editorial"):
    df = scrape_artsy_editorial()
    df.to_csv(f"{DATA_FOLDER}/artsy_editorial.csv", index=False)
    st.success(f"Scraped {len(df)} editorial headlines from Artsy.")
    st.dataframe(df)

if st.sidebar.button("Scrape Frieze Articles"):
    df = scrape_frieze_articles()
    df.to_csv(f"{DATA_FOLDER}/frieze.csv", index=False)
    st.success(f"Scraped {len(df)} Frieze articles.")
    st.dataframe(df)

if st.sidebar.button("Scrape UK/IT Galleries"):
    df = scrape_all_galleries()
    df.to_csv(f"{DATA_FOLDER}/gallery_names.csv", index=False)
    st.success(f"Scraped {len(df)} artist/show names from galleries.")
    st.dataframe(df)

if st.sidebar.button("Scrape Instagram Hashtags"):
    df = scrape_instagram_hashtag_preview("emergingartistuk")
    df.to_csv(f"{DATA_FOLDER}/instagram_usernames.csv", index=False)
    st.success(f"Scraped {len(df)} usernames from Instagram hashtag.")
    st.dataframe(df)

# ---------- Google News Tracker ----------
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔎 Google News Monitor")
artist_input = st.sidebar.text_input("Enter artist name")
if st.sidebar.button("Track News for Artist"):
    if artist_input:
        df = scrape_google_news(artist_input)
        st.success(f"Found {len(df)} news items for {artist_input}.")
        st.dataframe(df)
    else:
        st.warning("Enter an artist name to track news.")

# ---------- Main Area ----------
st.markdown("---")
st.header("📊 Summary (click scraper buttons to populate data)")

for file in os.listdir(DATA_FOLDER):
    if file.endswith(".csv"):
        file_path = os.path.join(DATA_FOLDER, file)
        try:
            df = pd.read_csv(file_path)
            if not df.empty:
                st.subheader(f"📁 {file}")
                st.dataframe(df)
            else:
                st.warning(f"{file} is currently empty.")
        except pd.errors.EmptyDataError:
            st.warning(f"{file} could not be read (no columns or malformed).")
