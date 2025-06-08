# scraper_suite.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import feedparser


# ---------- 1. ArtRabbit Scraper ----------
def scrape_artrabbit():
    urls = {
        "UK": "https://www.artrabbit.com/events/search?location=united-kingdom&tag=emerging",
        "Italy": "https://www.artrabbit.com/events/search?location=italy&tag=emerging"
    }
    all_data = []
    headers = {"User-Agent": "Mozilla/5.0"}

    for region, url in urls.items():
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        events = soup.find_all('div', class_='event-title-wrapper')

        for event in events:
            title_tag = event.find('a', class_='event-title')
            if title_tag:
                title = title_tag.text.strip()
                link = "https://www.artrabbit.com" + title_tag.get('href')
                name = title.replace('Group Exhibition:', '').replace('Solo Exhibition:', '').strip()
                all_data.append({
                    "artist_or_title": name,
                    "region": region,
                    "event_url": link,
                    "source": "ArtRabbit",
                    "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                })

    return pd.DataFrame(all_data)


# ---------- 2. Artsy Editorial Scraper (basic headline matcher) ----------
def scrape_artsy_editorial():
    url = "https://www.artsy.net/articles"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    articles = soup.find_all('a', class_='Box-sc-kv6pi1-0')
    data = []
    for article in articles:
        title = article.text.strip()
        href = article.get('href')
        if "trending" in title.lower() or "emerging" in title.lower():
            data.append({
                "article_title": title,
                "article_url": f"https://www.artsy.net{href}",
                "source": "Artsy Editorial",
                "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            })

    return pd.DataFrame(data)


# ---------- 3. Frieze Article Scraper ----------
def scrape_frieze_articles():
    url = "https://www.frieze.com/latest"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    items = soup.find_all('a', class_='link-tile__link')
    data = []
    for item in items:
        title = item.find('span', class_='link-tile__headline')
        if title and any(word in title.text.lower() for word in ["studio", "emerging", "artist"]):
            data.append({
                "article_title": title.text.strip(),
                "article_url": "https://www.frieze.com" + item.get('href'),
                "source": "Frieze",
                "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
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
