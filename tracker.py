import requests
from bs4 import BeautifulSoup 
from datetime import datetime
import random
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("tracker.log"), #log to tracker.log
        logging.StreamHandler() #log to console
    ]
)

def search_pastes(keywords):
    #grab pastes from pastebin archive
    url = "https://pastebin.com/archive"
    #spoofed user-agent header to get past less sophisticated bot blockers
    headers = {"User-Agent": random.choice(load_filepath('user-agents.txt', lowercase=False))}
    logging.info("Fetching recent pastes...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        logging.error(f"Failed to fetch Pastebin archive. Status code: {response.status_code}")
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
        try:
            paste_response = requests.get(paste_url, headers=headers)
            paste_response.raise_for_status() #raise error for bad status codes instead of just checking for 200
        except requests.exceptions.RequestException as e:
            logging.warning(f"Failed to fetch paste at {paste_url}. Error: {e}")
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
        logging.error(f"File not found: {filepath}")
        return []

def main():
    while True:
        logging.info("Starting search for new pastes...")
        results = search_pastes(load_filepath('keywords.txt'))
        if not results:
            logging.info("No new paste matches found.")
        for result in results:
            logging.info(f"Matched keyword '{result['keyword']}'")
            logging.info(f"FOUND: {result['title']} at {result['url']}")
            logging.info(f"Snippet: {result['snippet']}\n")
        logging.info("Completed search cycle. Waiting for the next cycle.")

if __name__ == "__main__":
    main()