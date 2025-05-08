import requests
from bs4 import BeautifulSoup 
from datetime import datetime
import random

def search_pastes(keywords):
    #grab pastes from pastebin archive
    url = "https://pastebin.com/archive"
    #spoofed user-agent header to get past less sophisticated bot blockers
    headers = {"User-Agent": random.choice(load_filepath('user-agents.txt', lowercase=False))}
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
        content = paste_soup.find("ol")
        #previously content_div = paste_soup.find("textarea", {"id": "paste_code"})
        ## pastebin changed html layout from textareas to ordered lists to mimic a code editor

        #new loop for searching keywords
        if content:
            paste_text = "\n".join(li.get_text() for li in content.find_all('li')).lower()
            for keyword in keywords:
                if keyword in paste_text:
#                    print(f"Matched keyword '{keyword}'")
                    results.append({
                        "keyword": keyword,
                        "title": paste_title,
                        "url": paste_url,
                        "snippet": paste_text[:300]
                    })

    return results

# went ahead and made this reusable since we're pulling two different lists
def load_filepath(filepath, lowercase=False):
    try:
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file if line.strip()]
            return [line.lower() for line in lines] if lowercase else lines
    except FileNotFoundError:
        print(f"[{datetime.now()}] File not found: {filepath}")
        return []

def main():
    while True:
        results = search_pastes(load_filepath('keywords.txt'))
        for result in results:
            print(f"Matched keyword: '{result['keyword']}'")
            print(f"FOUND: {result['title']} at {result['url']}")
            print(f"Snippet: {result['snippet']}\n")

if __name__ == "__main__":
    main()