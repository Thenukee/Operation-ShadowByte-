import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from openpyxl import Workbook

# Define QueryStatus class
class QueryStatus:
    CLAIMED = "Claimed"
    AVAILABLE = "Available"
    UNKNOWN = "Unknown"
    ILLEGAL = "Illegal"
    WAF = "WAF"

# Define QueryResult class
class QueryResult:
    def __init__(self, site_name, site_url_user, status, query_time=None):
        self.site_name = site_name
        self.site_url_user = site_url_user
        self.status = status
        self.query_time = query_time

    def __str__(self):
        status = str(self.status)
        return status

# Define QueryNotifyPrint class for logging
class QueryNotifyPrint:
    def __init__(self, verbose=False, print_all=False):
        self.verbose = verbose
        self.print_all = print_all

    def start(self, message):
        print(f"Checking articles for {message} on:")

    def update(self, result):
        response_time_text = f" [{round(result.query_time * 1000)}ms]" if result.query_time and self.verbose else ""
        if result.status == QueryStatus.CLAIMED:
            print(f"[+] {result.site_name}: {result.site_url_user}{response_time_text}")
        elif result.status == QueryStatus.AVAILABLE and self.print_all:
            print(f"[-] {result.site_name}: Not Found!")
        elif result.status == QueryStatus.UNKNOWN and self.print_all:
            print(f"[-] {result.site_name}: Unknown Error")
        elif result.status == QueryStatus.ILLEGAL and self.print_all:
            print(f"[-] {result.site_name}: Illegal Username Format")
        elif result.status == QueryStatus.WAF and self.print_all:
            print(f"[-] {result.site_name}: Blocked by bot detection (proxy may help)")

    def finish(self, message="The processing has been finished."):
        print(f"[*] {message}")

# Define functions to scrape each news site
def scrape_daily_news(username, start_year, end_year):
    url = "https://www.dailynews.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        headline_tag = article.find('h3')
        if headline_tag and username.lower() in headline_tag.text.lower():
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.dailynews.lk' + article_url
            publication_date = article.find('time').text.strip()
            article_date = datetime.strptime(publication_date, "%Y-%m-%d")

            if start_year <= article_date.year <= end_year:
                articles.append(QueryResult("Daily News", article_url, QueryStatus.CLAIMED))
    return articles

def scrape_daily_mirror(username, start_year, end_year):
    url = "https://www.dailymirror.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        headline_tag = article.find('h2')
        if headline_tag and username.lower() in headline_tag.text.lower():
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.dailymirror.lk' + article_url
            publication_date = article.find('time').text.strip()
            article_date = datetime.strptime(publication_date, "%Y-%m-%d")

            if start_year <= article_date.year <= end_year:
                articles.append(QueryResult("Daily Mirror", article_url, QueryStatus.CLAIMED))
    return articles

def scrape_sunday_observer(username, start_year, end_year):
    url = "https://www.sundayobserver.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        headline_tag = article.find('h2')
        if headline_tag and username.lower() in headline_tag.text.lower():
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.sundayobserver.lk' + article_url
            publication_date = article.find('time').text.strip()
            article_date = datetime.strptime(publication_date, "%Y-%m-%d")

            if start_year <= article_date.year <= end_year:
                articles.append(QueryResult("Sunday Observer", article_url, QueryStatus.CLAIMED))
    return articles

def scrape_adaderana(username, start_year, end_year):
    url = "https://www.adaderana.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        headline_tag = article.find('h3')
        if headline_tag and username.lower() in headline_tag.text.lower():
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.adaderana.lk' + article_url
            publication_date = article.find('time').text.strip()
            article_date = datetime.strptime(publication_date, "%Y-%m-%d")

            if start_year <= article_date.year <= end_year:
                articles.append(QueryResult("Ada Derana", article_url, QueryStatus.CLAIMED))
    return articles

def scrape_sunday_times(username, start_year, end_year):
    url = "https://www.sundaytimes.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        headline_tag = article.find('h2')
        if headline_tag and username.lower() in headline_tag.text.lower():
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.sundaytimes.lk' + article_url
            publication_date = article.find('time').text.strip()
            article_date = datetime.strptime(publication_date, "%Y-%m-%d")

            if start_year <= article_date.year <= end_year:
                articles.append(QueryResult("Sunday Times", article_url, QueryStatus.CLAIMED))
    return articles

def scrape_the_island(username, start_year, end_year):
    url = "https://www.island.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        headline_tag = article.find('h2')
        if headline_tag and username.lower() in headline_tag.text.lower():
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.island.lk' + article_url
            publication_date = article.find('time').text.strip()
            article_date = datetime.strptime(publication_date, "%Y-%m-%d")

            if start_year <= article_date.year <= end_year:
                articles.append(QueryResult("The Island", article_url, QueryStatus.CLAIMED))
    return articles

def main(username, start_year, end_year):
    sites = {
        "Daily News": scrape_daily_news,
        "Daily Mirror": scrape_daily_mirror,
        "Sunday Observer": scrape_sunday_observer,
        "Ada Derana": scrape_adaderana,
        "Sunday Times": scrape_sunday_times,
        "The Island": scrape_the_island
    }
    
    notifier = QueryNotifyPrint(verbose=True, print_all=True)
    notifier.start(username)
    
    all_results = []
    for site_name, scrape_func in sites.items():
        results = scrape_func(username, start_year, end_year)
        for result in results:
            notifier.update(result)
            all_results.append([site_name, result.site_url_user, result.status])
    
    notifier.finish()
    
    # Save results to Excel
    df = pd.DataFrame(all_results, columns=["Site", "URL", "Status"])
    output_file = "scraping_results.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    username = input("Enter the person's name: ")
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    main(username, start_year, end_year)
