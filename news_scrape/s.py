import requests
from bs4 import BeautifulSoup
import time

def search_ada_derana(name):
    query = '+'.join(name.split())
    URL = f'https://www.adaderana.lk/search_results.php?mode=0&show=1&query={query}'
    response = requests.get(URL)
    print("Ada Derana Response code is:", response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = (
            soup.find_all('h1') +
            soup.find_all('h2') +
            soup.find_all('h3') +
            soup.find_all('h4') +
            soup.find_all('h5') +
            soup.find_all('h6')
        )
        if headlines:
            for headline in headlines:
                print("Ada Derana:", headline.text.strip())
                time.sleep(1)
        else:
            print("Ada Derana: not found")
    else:
        print("Failed to retrieve the page from Ada Derana.")



def search_daily_mirror_epaper(name):
    query = '%20'.join(name.split())
    URL = f'https://dailymirrorepaper.pressreader.com/search?query={query}&newspapers=8610&hideSimilar=1&type=3&state=4'
    response = requests.get(URL)
    print("Daily Mirror E-paper Response code is:", response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        headlines = (
            soup.find_all('h1') +
            soup.find_all('h2') +
            soup.find_all('h3') +
            soup.find_all('h4') +
            soup.find_all('h5') +
            soup.find_all('h6')
        )
        if headlines:
            for headline in headlines:
                print("Daily Mirror E-paper:", headline.text.strip())
                time.sleep(1)
        else:
            print("Daily Mirror E-paper: not found")
    else:
        print("Failed to retrieve the page from Daily Mirror E-paper.")

# Input person's name
person_name = input("Enter the person's name to search for: ")


# Search on all websites
search_ada_derana(person_name)

search_daily_mirror_epaper(person_name)

