import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def search_person(name, start_year, end_year):
    # Encode the person's name for URL
    query = '+'.join(name.split())
    URL = f'https://www.adaderana.lk/search_results.php?mode=2&show=1&query={query}'
    
    # Request the website
    response = requests.get(URL)
    print("The Response code is:", response.status_code)
    
    if response.status_code == 200:
        # Parse the HTML document
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract news headlines and content
        results = soup.find_all('div', class_='news-item')  # Adjust class based on Ada Derana's HTML structure
        
        # Display the headlines and their URLs
        for result in results:
            headline = result.find('h4')  # Adjust based on actual HTML structure
            if headline:
                print("Headline:", headline.text.strip())
            
            content = result.find('p')  # Adjust based on actual HTML structure
            if content:
                print("Content:", content.text.strip())
            
            link = result.find('a')
            if link:
                print("URL:", link['href'])  # Get URL if available
            
            # Extract and filter by date
            date_str = result.find('span', class_='date')  # Adjust class based on actual HTML structure
            if date_str:
                try:
                    # Adjust date format based on actual HTML structure
                    article_date = datetime.strptime(date_str.text.strip(), '%d %b %Y')
                    if start_year <= article_date.year <= end_year:
                        print("Date:", article_date.strftime('%d %b %Y'))
                        print("\n")
                except ValueError:
                    # Handle date parsing errors
                    print("Date format error:", date_str.text.strip())
            
            time.sleep(1)
    else:
        print("Failed to retrieve the page.")

# Input person's name
person_name = input("Enter the person's name to search for: ")

# Input start and end years
start_year = int(input("Enter the starting year (YYYY): "))
end_year = int(input("Enter the ending year (YYYY): "))

# Search for the person within the specified year range
search_person(person_name, start_year, end_year)
