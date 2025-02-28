import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

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

def save_html(html, filename="tmp.html"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

def extract_hyperlinks(filename="tmp.html", base_url="https://www.cnn.com"):
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    links = []
    for a_tag in soup.find_all("a", href=True):
        text = a_tag.get_text(strip=True)
        href = a_tag["href"]
        if text and len(text.split()) >= 5:  # Only store links with at least 5 words in text
            if href.startswith("/"):
                href = base_url + href  # Prepend base URL if link is relative
            links.append((text, href))
    
    return links

def save_links(links, filename="links.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for text, link in links:
            file.write(f"{text}: {link}\n")

def print_dates():
    today = datetime.now().strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"Today's date: {today}")
    print(f"Yesterday's date: {yesterday}")

def main():
    print_dates()
    url = "https://www.cnn.com"
    print(f"Fetching page: {url}")
    html = fetch_page(url)
    save_html(html)
    print("HTML saved to tmp.html")
    
    links = extract_hyperlinks()
    save_links(links)
    print("Extracted hyperlinks saved to links.txt")
    
if __name__ == "__main__":
    main()
