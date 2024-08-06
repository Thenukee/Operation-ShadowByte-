import requests
from bs4 import BeautifulSoup
import time

def search_person(name):
    # Encode the person's name for URL
    query = '+'.join(name.split())
    URL = f'https://www.adaderana.lk/search_results.php?mode=2&show=1&query={query}'
    
    # Request the website
    response = requests.get(URL)
    print("The Response code is :", response.status_code)
    
    if response.status_code == 200:
        # Parse the HTML document
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract news headlines and content
        results = soup.find_all('div', class_='news-item') # Adjust class based on Ada Derana's HTML structure
        
        # Display the headlines and their URLs
        for result in results:
            headline = result.find('h4')  # Adjust based on actual HTML structure
            if headline:
                print("Headline:", headline.text.strip())
            
            content = result.find('p')  # Adjust based on actual HTML structure
            if content:
                print("Content:", content.text.strip())
            
            print("URL:", result.find('a')['href'])  # Get URL if available
            print("\n")
            time.sleep(1)
    else:
        print("Failed to retrieve the page.")

# Input person's name
person_name = input("Enter the person's name to search for: ")
search_person(person_name)
