import requests
from bs4 import BeautifulSoup

def check_email_pwned(email):
    # Create the URL for the search
    url = f"https://haveibeenpwned.com/search/{email}"
    
    # Send a request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the relevant section that indicates whether the email is pwned
        results = soup.find('div', {'id': 'pwned-list'})
        if results:
            # If results are found, extract details
            pwned = True
            breaches = results.find_all('li')
            details = [breach.get_text(strip=True) for breach in breaches]
        else:
            # If no results are found, the email is not pwned
            pwned = False
            details = []
    else:
        # Handle errors
        print("Error fetching the data")
        return None, None
    
    return pwned, details

if __name__ == "__main__":
    email = input("Enter the email to check: ")
    pwned, details = check_email_pwned(email)
    
    if pwned:
        print(f"The email {email} has been pwned!")
        print("Details of breaches:")
        for detail in details:
            print(detail)
    else:
        print(f"The email {email} has not been pwned.")