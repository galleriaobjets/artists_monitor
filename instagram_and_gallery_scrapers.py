# instagram_and_gallery_scrapers.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import re

# ---------- 5. Hashtag Scraper (Instagram via Apify or HTML fallback) ----------
# NOTE: Actual Instagram scraping at scale requires a paid service or Puppeteer

def scrape_instagram_hashtag_preview(hashtag):
    """
    Simulates scraping a few top posts from a public Instagram hashtag page.
    In production, use Apify or Instaloader with proxies.
    """
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return pd.DataFrame([])

        usernames = list(set(re.findall(r'"username":"(.*?)"', response.text)))
        return pd.DataFrame({
            "hashtag": hashtag,
            "username": usernames,
            "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        print(f"Error scraping hashtag {hashtag}: {e}")
        return pd.DataFrame([])


# ---------- 6. Gallery Exhibition Scraper (UK/IT sample gallery pages) ----------

def scrape_gallery_page(url, gallery_name):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = []
    for link in soup.find_all('a'):
        text = link.get_text(strip=True)
        href = link.get('href')
        if href and text and len(text.split()) <= 5:  # Likely a name
            data.append({
                "artist_or_title": text,
                "gallery": gallery_name,
                "source_url": url,
                "scraped_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            })

    return pd.DataFrame(data)


def scrape_all_galleries():
    galleries = [
        ("https://studiovoltaire.org/whats-on/", "Studio Voltaire"),
        ("https://www.francescaminini.it/exhibitions/", "Francesca Minini"),
        ("https://www.galleriacontinua.com/exhibitions", "Galleria Continua")
    ]

    all_data = pd.DataFrame()
    for url, name in galleries:
        df = scrape_gallery_page(url, name)
        all_data = pd.concat([all_data, df], ignore_index=True)

    return all_data


# ---------- Example Runner ----------
if __name__ == "__main__":
    hashtag_df = scrape_instagram_hashtag_preview("emergingartistuk")
    print("Instagram usernames from hashtag:", hashtag_df.head())

    gallery_df = scrape_all_galleries()
    print("Artists from gallery pages:", gallery_df.head())
