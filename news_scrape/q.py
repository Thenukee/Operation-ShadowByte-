import requests
from bs4 import BeautifulSoup
import time

def search_ada_derana(name):
    # Encode the person's name for URL
    query = '+'.join(name.split())
    URL = f'https://www.adaderana.lk/search_results.php?mode=0&show=1&query={query}'
    
    # Request the website
    response = requests.get(URL)
    print("Ada Derana Response code is:", response.status_code)
    
    if response.status_code == 200:
        # Parse the HTML document
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the news headlines
        headlines = (
            soup.find_all('h1') +
            soup.find_all('h2') +
            soup.find_all('h3') +
            soup.find_all('h4') +
            soup.find_all('h5') +
            soup.find_all('h6')
        )
        
        if headlines:
            # Display the headlines
            for headline in headlines:
                print("Ada Derana:", headline.text.strip())
                time.sleep(1)
        else:
            print("Ada Derana: not found")
    else:
        print("Failed to retrieve the page from Ada Derana.")

def search_sunday_observer(name):
    # Encode the person's name for URL
    query = '+'.join(name.split())
    URL = f'https://www.sundayobserver.lk/?s={query}'
    
    # Request the website
    response = requests.get(URL)
    print("Sunday Observer Response code is:", response.status_code)
    
    if response.status_code == 200:
        # Parse the HTML document
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the news headlines
        headlines = (
            soup.find_all('h1') +
            soup.find_all('h2') +
            soup.find_all('h3') +
            soup.find_all('h4') +
            soup.find_all('h5') +
            soup.find_all('h6')
        )
        
        if headlines:
            # Display the headlines
            for headline in headlines:
                print("Sunday Observer:", headline.text.strip())
                time.sleep(1)
        else:
            print("Sunday Observer: not found")
    else:
        print("Failed to retrieve the page from Sunday Observer.")

def search_daily_mirror(name):
    # Encode the person's name for URL
    query = '+'.join(name.split())
    URL = f'https://www.dailymirror.lk/search?query={query}'
    
    # Request the website
    response = requests.get(URL)
    print("Daily Mirror Response code is:", response.status_code)
    
    if response.status_code == 200:
        # Parse the HTML document
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the news headlines
        headlines = (
            soup.find_all('h1') +
            soup.find_all('h2') +
            soup.find_all('h3') +
            soup.find_all('h4') +
            soup.find_all('h5') +
            soup.find_all('h6')
        )
        
        if headlines:
            # Display the headlines
            for headline in headlines:
                print("Daily Mirror:", headline.text.strip())
                time.sleep(1)
        else:
            print("Daily Mirror: not found")
    else:
        print("Failed to retrieve the page from Daily Mirror.")

# Input person's name
person_name = input("Enter the person's name to search for: ")

# Search on all websites
search_ada_derana(person_name)
search_sunday_observer(person_name)
search_daily_mirror(person_name)
