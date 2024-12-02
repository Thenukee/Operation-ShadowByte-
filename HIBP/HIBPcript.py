import requests
from bs4 import BeautifulSoup

def check_email_breaches(email):
    url = f"https://haveibeenpwned.com/unifiedsearch/{email}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Parse the HTML to find breach data (depends on the page structure)
            # Note: This part would need updates if HIBP changes its layout
            return soup.prettify()
        elif response.status_code == 404:
            return "No breaches found."
        else:
            return f"Unexpected response: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

if __name__ == "__main__":
    email = input("Enter the email address to check: ")
    result = check_email_breaches(email)
    print(result)
