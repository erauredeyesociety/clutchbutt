import requests
import random
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import unicodedata
import re
import os

# Required packages: requests, beautifulsoup4
# Install using: pip install requests beautifulsoup4

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
]

def fetch_page(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    return response.text

def save_html(html, filename):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

def clean_text(text):
    # Normalize all Unicode characters
    text = unicodedata.normalize("NFKD", text)
    return text

def extract_hyperlinks(filename="tmp.html", base_url="https://www.cnn.com"):
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    links = []
    for a_tag in soup.find_all("a", href=True):
        text = clean_text(a_tag.get_text(strip=True))
        href = a_tag["href"]
        if text and len(text.split()) >= 5:  # Only store links with at least 5 words in text
            if href.startswith("/"):
                href = base_url + href  # Prepend base URL if link is relative
            links.append({"date": datetime.now().strftime("%Y-%m-%d"), "headline": text, "link": href})
    
    return links

def load_history(filename="links_history.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                if "daily_links" not in data or "history_links" not in data:
                    data = {"daily_links": [], "history_links": []}
            except json.JSONDecodeError:
                data = {"daily_links": [], "history_links": []}
    else:
        data = {"daily_links": [], "history_links": []}
    return data

def save_history(data, filename="links_history.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def manage_history():
    data = load_history()
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Move old daily links to history if they are not from today
    if data["daily_links"] and data["daily_links"][0]["date"] != today:
        data["history_links"] = data["daily_links"] + data["history_links"]
        data["daily_links"] = []
    
    # Keep only links from the last 4 weeks in history
    four_weeks_ago = datetime.now() - timedelta(days=28)
    data["history_links"] = [link for link in data["history_links"] if datetime.strptime(link["date"], "%Y-%m-%d") >= four_weeks_ago]
    
    return data


def main():
    url = "https://www.cnn.com"
    print(f"Fetching page: {url}")
    html = fetch_page(url)
    save_html(html)
    print("HTML saved to tmp.html")
    
    links = extract_hyperlinks()
    data = manage_history()
    data["daily_links"].extend(links)
    save_history(data)
    print("Updated links saved to links_history.json")
    
if __name__ == "__main__":
    main()
