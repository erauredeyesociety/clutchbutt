import requests
import random
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

# List of user agents to rotate
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
]

# Example structure of links dictionary (already defined)
links = {
    "CNN": "https://www.cnn.com",
    "BBC": "https://www.bbc.com",
    "NYTimes": "https://www.nytimes.com"
}

def fetch_page(url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    return response.text

def save_html(html, website):
    # Ensure the tmp_html directory exists
    os.makedirs("tmp_html", exist_ok=True)
    
    # Save HTML as <website>_tmp.html inside tmp_html/
    filepath = os.path.join("tmp_html", f"{website}_tmp.html")
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(html)

def clean_text(text):
    # This function can be customized to clean text if necessary
    return text.strip()

def extract_hyperlinks(filename, base_url):
    with open(filename, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
    
    links_data = {}
    for a_tag in soup.find_all("a", href=True):
        text = clean_text(a_tag.get_text(strip=True))
        href = a_tag["href"]
        
        # Check if the link matches any of the pre-defined websites
        for name, base_url in links.items():
            if href.startswith(base_url) or href.startswith("/"):  # Check if the link starts with the base URL
                if href.startswith("/"):  # Handle relative URLs by prepending base URL
                    href = base_url + href
                
                # Only store links with at least 5 words in text
                if len(text.split()) >= 5:
                    if name not in links_data:
                        links_data[name] = []  # Initialize the list if not already there
                    
                    links_data[name].append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "headline": text,
                        "link": href
                    })
                break  # Move to the next link once a match is found
    
    return links_data

def load_existing_links(filename="links.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {"daily_links": {}, "history_links": {}}

def update_history_links(existing_links, current_date):
    history_links = existing_links.get("history_links", {})
    
    # Remove links older than 4 weeks
    cutoff_date = datetime.now() - timedelta(weeks=4)
    cutoff_date_str = cutoff_date.strftime("%Y-%m-%d")
    
    for website, links in history_links.items():
        history_links[website] = [link for link in links if link["date"] >= cutoff_date_str]

    return history_links

def save_links(links_data, filename="links.json"):
    # Load existing data to append to it
    existing_links = load_existing_links(filename)
    
    # Append new daily links to existing daily links
    for website, new_links in links_data.items():
        if website not in existing_links["daily_links"]:
            existing_links["daily_links"][website] = []  # Initialize list if not already there
        existing_links["daily_links"][website].extend(new_links)  # Append the new links

    # Move any non-today links to history_links
    history_links = update_history_links(existing_links, datetime.now().strftime("%Y-%m-%d"))
    
    # Append non-today links to history_links
    for website, links in links_data.items():
        for link in links:
            if link["date"] != datetime.now().strftime("%Y-%m-%d"):
                if website not in history_links:
                    history_links[website] = []
                history_links[website].append(link)
    
    # Save both sections (daily_links and history_links) to the JSON file
    existing_links["history_links"] = history_links

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(existing_links, file, indent=4)

def main():
    # Loop through the links dictionary
    for website, base_url in links.items():
        print(f"Fetching page: {base_url}")
        
        # Fetch HTML content for each website
        html = fetch_page(base_url)
        save_html(html, website)  # Save HTML as <website>_tmp.html inside tmp_html/
        
        # Extract hyperlinks from the saved HTML file
        links_data = extract_hyperlinks(f"tmp_html/{website}_tmp.html", base_url)
        
        # Save the extracted links to a JSON file
        save_links(links_data)
        print(f"Extracted hyperlinks for {website} saved to links.json")
        
if __name__ == "__main__":
    main()
