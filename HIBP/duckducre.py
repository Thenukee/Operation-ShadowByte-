import requests
from bs4 import BeautifulSoup
import time

def scrape_duckduckgo(query):
    url = f"https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    data = {"q": query}
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        results = []
        for result in soup.find_all("a", class_="result__a"):
            title = result.text
            link = result["href"]
            results.append({"title": title, "link": link})
        return results
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Example: Searching for an email address
if __name__ == "__main__":
    email = input("Enter the email address to search: ")
    query = f'"{email}"'
    results = scrape_duckduckgo(query)
    print("Results:")
    for result in results:
        print(f"- {result['title']}: {result['link']}")
        time.sleep(1)  # Avoid sending requests too quickly
