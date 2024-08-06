import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

news_list = []

class QueryStatus:
    CLAIMED = "Found"
    AVAILABLE = "Not Found"
    UNKNOWN = "Unknown Error"
    ILLEGAL = "Illegal"
    WAF = "Blocked by bot detection"

class QueryResult:
    def __init__(self, site_name, site_url_user, status, query_time=None):
        self.site_name = site_name
        self.site_url_user = site_url_user
        self.status = status
        self.query_time = query_time

    def __str__(self):
        status = str(self.status)
        return status

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

def fetch_articles_from_site(url, notifier, site_name, search_name, start_year, end_year):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    articles_found = False
    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip() if article.find('h2') else article.find('h3').text.strip()
            if search_name.lower() in headline.lower():
                publication_date = article.find('time').text.strip()
                article_year = datetime.strptime(publication_date, "%B %d, %Y").year  # Adjust date format as needed
                if start_year <= article_year <= end_year:
                    article_url = article.find('a')['href'].strip()
                    if not article_url.startswith('http'):
                        article_url = url + article_url
                    news_list.append({
                        'Newspaper': site_name,
                        'Article URL': article_url,
                        'Headline': headline,
                        'Publication Date': publication_date
                    })
                    articles_found = True
                    notifier.update(QueryResult(site_name, article_url, QueryStatus.CLAIMED))
        except Exception as e:
            notifier.update(QueryResult(site_name, url, QueryStatus.UNKNOWN))
            print(f"An error occurred: {e}")

    if not articles_found:
        notifier.update(QueryResult(site_name, url, QueryStatus.AVAILABLE))

def fetch_all_articles(notifier, search_name, start_year, end_year):
    fetch_articles_from_site("https://www.dailynews.lk/", notifier, "Daily News", search_name, start_year, end_year)
    fetch_articles_from_site("https://www.dailymirror.lk/", notifier, "Daily Mirror", search_name, start_year, end_year)
    fetch_articles_from_site("https://www.sundayobserver.lk/", notifier, "Sunday Observer", search_name, start_year, end_year)
    fetch_articles_from_site("https://www.adaderana.lk/", notifier, "Ada Derana", search_name, start_year, end_year)
    fetch_articles_from_site("https://www.sundaytimes.lk/", notifier, "Sunday Times", search_name, start_year, end_year)
    fetch_articles_from_site("https://www.island.lk/", notifier, "The Island", search_name, start_year, end_year)

    # Save to Excel
    df = pd.DataFrame(news_list)
    df.to_excel('GPSD.xlsx', index=False)

# Main function
def main(username, start_year, end_year):
    notifier = QueryNotifyPrint(verbose=True, print_all=True)
    notifier.start(username)

    fetch_all_articles(notifier, username, start_year, end_year)
    
    notifier.finish()
    print("Articles have been fetched and saved to GPSD.xlsx")

if __name__ == "__main__":
    username = input("Enter the person's name: ")
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    main(username, start_year, end_year)
