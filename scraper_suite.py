# scraper_suite.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import feedparser


import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# ---------- 1. ArtRabbit Scraper ----------
def scrape_artrabbit():
    url = "https://www.artrabbit.com/events/search?city=London"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    print("Fetching ArtRabbit events...")
    res = requests.get(url, headers=headers)
    print(f"Status code: {res.status_code}")
    print(f"Content preview: {res.text[:500]}")

    soup = BeautifulSoup(res.text, "html.parser")
    events = soup.select(".event-list__item")
    data = []

    for event in events:
        title = event.select_one(".event-title")
        venue = event.select_one(".event-venue")
        date = event.select_one(".event-date")

        data.append({
            "title": title.text.strip() if title else "N/A",
            "venue": venue.text.strip() if venue else "N/A",
            "date": date.text.strip() if date else "N/A",
            "scraped_at": datetime.utcnow()
        })

    return pd.DataFrame(data)


# ---------- 2. Artsy Editorial Scraper ----------
def scrape_artsy_editorial():
    url = "https://www.artsy.net/editorial"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    print("Fetching Artsy Editorial...")
    res = requests.get(url, headers=headers)
    print(f"Status code: {res.status_code}")
    print(f"Content preview: {res.text[:500]}")

    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select("a[href*='/article/']")
    data = []

    for art in articles:
        title = art.text.strip()
        href = art["href"]
        data.append({
            "title": title,
            "url": f"https://www.artsy.net{href}",
            "scraped_at": datetime.utcnow()
        })

    return pd.DataFrame(data)


# ---------- 3. Frieze Articles Scraper ----------
def scrape_frieze_articles():
    url = "https://www.frieze.com/latest"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    print("Fetching Frieze articles...")
    res = requests.get(url, headers=headers)
    print(f"Status code: {res.status_code}")
    print(f"Content preview: {res.text[:500]}")

    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.select(".card--teaser")
    data = []

    for article in articles:
        title = article.select_one(".card__title")
        link = article.find("a", href=True)
        data.append({
            "title": title.text.strip() if title else "N/A",
            "url": f"https://www.frieze.com{link['href']}" if link else "N/A",
            "scraped_at": datetime.utcnow()
        })

    return pd.DataFrame(data)


# ---------- 4. Google News Scraper via RSS ----------
def scrape_google_news(artist_name):
    rss_url = f"https://news.google.com/rss/search?q={artist_name.replace(' ', '+')}+artist"
    feed = feedparser.parse(rss_url)

    data = []
    for entry in feed.entries:
        data.append({
            "artist_name": artist_name,
            "headline": entry.title,
            "url": entry.link,
            "published": entry.published,
            "source": "Google News RSS"
        })

    return pd.DataFrame(data)


# ---------- Example Runner ----------
if __name__ == "__main__":
    artrabbit_df = scrape_artrabbit()
    artsy_df = scrape_artsy_editorial()
    frieze_df = scrape_frieze_articles()

    print("ArtRabbit:", artrabbit_df.head())
    print("Artsy Editorial:", artsy_df.head())
    print("Frieze:", frieze_df.head())

    # Example for one artist (to be looped later)
    news_df = scrape_google_news("Marco Neri")
    print("Google News for Marco Neri:", news_df.head())
