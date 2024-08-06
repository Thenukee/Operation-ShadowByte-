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

def search_daily_news(name):
    query = '+'.join(name.split())
    URL = f'https://www.dailynews.lk/?s={query}'  #https://www.dailynews.lk/?s=DHAMMIKA
    response = requests.get(URL)
    print("Daily News Response code is:", response.status_code)
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
                print("Daily News:", headline.text.strip())
                time.sleep(1)
        else:
            print("Daily News: not found")
    else:
        print("Failed to retrieve the page from Daily News.")

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

def search_sunday_observer_epaper(name, date, page_id):
    base_url = 'https://epaper.dailynews.lk/SundayObserver' #https://www.sundayobserver.lk/?s={search_term_string}
    params = {
        'eid': '2',
        'edate': date,
        'pgid': page_id,
        'device': 'desktop',
        'view': '2'
    }
    response = requests.get(base_url, params=params)
    print("Sunday Observer E-paper Response code is:", response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = soup.find_all('article')
        found = False
        for article in articles:
            if name.lower() in article.text.lower():
                headline = article.find('h1') or article.find('h2') or article.find('h3') or article.find('h4') or article.find('h5') or article.find('h6')
                if headline:
                    print("Sunday Observer E-paper:", headline.text.strip())
                    found = True
                    time.sleep(1)
        if not found:
            print("Sunday Observer E-paper: not found")
    else:
        print("Failed to retrieve the page from Sunday Observer E-paper.")

def search_scribd(name):
    query = '+'.join(name.split())
    URL = f'https://www.scribd.com/search?query={query}'
    response = requests.get(URL)
    print("Scribd Response code is:", response.status_code)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Scribd's search results are structured differently; adjust as necessary
        titles = soup.find_all('h3')
        if titles:
            for title in titles:
                print("Scribd:", title.text.strip())
                time.sleep(1)
        else:
            print("Scribd: not found")
    else:
        print("Failed to retrieve the page from Scribd.")

# Input person's name
person_name = input("Enter the person's name to search for: ")


# Search on all websites
search_ada_derana(person_name)
search_daily_news(person_name)
search_daily_mirror_epaper(person_name)
search_sunday_observer_epaper(person_name)
search_scribd(person_name)

