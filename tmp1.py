import requests
import random

newsSites = {
    "AP News": "https://www.bbc.com/",
    "BBC": "apnews.com",
    "FOX News": "www.foxnews.com",
    "Wall Street Journal": "www.wsj.com",
    "Barrons": "www.barrons.com",
    "Forbes": "www.forbes.com",
    "CNN": "www.cnn.com",
    "CNBC": "www.cnbc.com",
    "Yahoo": "www.yahoo.com",
    "EPOCH Times": "www.theepochtimes.com",
    "Reuters": "www.reuters.com",
    https://www.nytimes.com/
    https://www.washingtonpost.com/
}

youtubes = {

}

government_branches = {
    https://www.dailypress.senate.gov/
    https://www.periodicalpress.senate.gov/
    https://progressives.house.gov/press-releases
    https://www.speaker.gov/category/press-releases/
    https://www.supremecourt.gov/publicinfo/press/pressreleases.aspx
    https://www.whitehouse.gov/briefings-statements/
    https://www.whitehouse.gov/news/
    https://home.treasury.gov/news/press-releases
    https://home.treasury.gov/news/press-releases/statements-remarks
}

military = {
    https://www.militarytimes.com/
    https://www.16af.af.mil/Newsroom/
    https://www.af.mil/News/
    https://www.army.mil/news/newsreleases
    https://www.marines.mil/News/Press-Releases/
    https://www.navy.mil/Press-Office/Press-Releases/
    https://www.news.uscg.mil/Press-Releases/
    https://www.spaceforce.mil/News/
    https://www.defense.gov/News/Releases/
    https://www.cybercom.mil/Media/News/
}

intelligence = {
    https://www.nsa.gov/Press-Room/Press-Releases-Statements/
    https://www.nsa.gov/Press-Room/Speeches-Testimony/
    https://www.dia.mil/News-Features/
    https://www.dia.mil/News-Features/Press-Releases/
    https://www.cia.gov/stories/press-releases-and-statements/
    https://www.fbi.gov/news/press-releases
    https://www.dea.gov/what-we-do/news/press-releases
    https://www.dea.gov/what-we-do/news/stories
    https://www.ice.gov/newsroom
    https://www.atf.gov/news/press-releases
    https://www.nro.gov/news-media-featured-stories/news-media-press-releases/
    https://www.dni.gov/index.php/348-newsroom/press-releases
    https://www.nga.mil/news/News.html
    https://www.state.gov/remarks-and-releases-bureau-of-intelligence-and-research
}

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

def main():
    url = "https://www.foxnews.com/"
    print(f"Fetching page: {url}")
    html = fetch_page(url)
    save_html(html)
    print("HTML saved to tmp.html")
    
if __name__ == "__main__":
    main()
