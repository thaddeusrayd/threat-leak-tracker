import time 
from datetime import datetime

#placeholder for future searching:
def search_pastes(keywords):
    print(f"[{datetime.now()}] Searching for: {', '.join(keywords)}")
    #simulate results:
    return [{"title": "Leaked credentials", "url": "http://example.com", "snippet": "admin:password123"}]

def main():
    keywords = ["example.com", "admin", "password"]
    while True:
        results = search_pastes(keywords)
        for result in results:
            print(f"FOUND: {result['title']} at {result['url']}")
            print(f"Snippet: {result['snippet']}\n")
        time.sleep(300) #check every 5min for now - placeholder

if __name__ == "__main__":
    main()