import requests

def search_duckduckgo(query):
    url = "https://api.duckduckgo.com/"
    params = {
        "q": query,
        "format": "json",
        "no_html": 1,
        "skip_disambig": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Example: Searching for an email address
if __name__ == "__main__":
    email = input("Enter the email address to search: ")
    query = f'"{email}"'
    results = search_duckduckgo(query)
    print("Results:")
    print(results)
