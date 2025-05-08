import requests
from bs4 import BeautifulSoup 
from datetime import datetime
import random

#fun addition -- providing user-agent header rotation functionality
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]
#fun fact - the inclusion of Mozilla is a Netscape artifact from when websites looked specifically for "Mozilla"
## when newer browsers came along, they faked their user-agent headers (like I'm doing here)
## I just learned this and thought it was wild

def search_pastes(keywords):
    #grab pastes from pastebin archive
    url = "https://pastebin.com/archive"
    #spoofed user-agent header to get past less sophisticated bot blockers
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    print(f"[{datetime.now()}] Fetching recent pastes...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch Pastebin archive.")
        return []
    #using BeautifulSoup mainly for error tolerance -- unreliable paste site HTML
    soup = BeautifulSoup(response.text, "html.parser")
    all_links = soup.select(".maintable a[href^='/']")
    paste_links = [link for link in all_links if "archive" not in link['href']][:5]


    results = []

    for link in paste_links:
        paste_url = f"https://pastebin.com{link['href']}"
        #get_text is a beautifulsoup method that extract only text; setting strip to true removes leading and trailing whitespace
        paste_title = link.get_text(strip=True)

        paste_response = requests.get(paste_url, headers=headers)
        if paste_response.status_code != 200:
            continue
        
        paste_soup = BeautifulSoup(paste_response.text, "html.parser")
        content_div = paste_soup.find("ol")

        #new loop for searching keywords
        if content_div:
            paste_text = content_div.get_text()
            for keyword in keywords:
                if keyword.lower() in paste_text.lower():
                    results.append({
                        "title": paste_title,
                        "url": paste_url,
                        "snippet": paste_text[:300]
                    })

    return results

def main():
    keywords = ["example.com", "admin", "password", "exploit", "accounts"]
    while True:
        results = search_pastes(keywords)
        for result in results:
            print(f"FOUND: {result['title']} at {result['url']}")
            print(f"Snippet: {result['snippet']}\n")
       # time.sleep(300) #check every 5min for now - placeholder

if __name__ == "__main__":
    main()