import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
import logging

class QueryStatus:
    CLAIMED = "claimed"
    AVAILABLE = "available"
    UNKNOWN = "unknown"
    ILLEGAL = "illegal"
    WAF = "waf"

class QueryResult:
    def __init__(self, site_name, site_url_user, status, query_time=None):
        self.site_name = site_name
        self.site_url_user = site_url_user
        self.status = status
        self.query_time = query_time

class QueryNotifyPrint:
    def __init__(self, result=None, verbose=False, print_all=False, browse=False):
        self.result = result
        self.verbose = verbose
        self.print_all = print_all
        self.browse = browse

    def start(self, message):
        print(f"Checking username {message} on:")
        print('\r')

    def update(self, result):
        self.result = result
        response_time_text = f" [{round(self.result.query_time * 1000)}ms]" if self.result.query_time and self.verbose else ""
        if result.status == QueryStatus.CLAIMED:
            print(f"[+] {self.result.site_name}: {self.result.site_url_user}{response_time_text}")
        elif result.status == QueryStatus.AVAILABLE and self.print_all:
            print(f"[-] {self.result.site_name}: Not Found!")
        elif result.status == QueryStatus.UNKNOWN and self.print_all:
            print(f"[-] {self.result.site_name}: Unknown Error")
        elif result.status == QueryStatus.ILLEGAL and self.print_all:
            print(f"[-] {self.result.site_name}: Illegal Username Format")
        elif result.status == QueryStatus.WAF and self.print_all:
            print(f"[-] {self.result.site_name}: Blocked by bot detection (proxy may help)")

    def finish(self, message="The processing has been finished."):
        print(f"[*] {message}")

def scrape_site(username, site_name, base_url):
    # Simulated scraping logic (replace with actual logic)
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Simulate finding articles
    articles = [
        {"headline": f"{username} in news", "url": f"{base_url}/article1", "date": "2024-01-01"},
        {"headline": f"Another article about {username}", "url": f"{base_url}/article2", "date": "2024-01-02"}
    ]
    
    results = []
    for article in articles:
        results.append(QueryResult(site_name, article["url"], QueryStatus.CLAIMED))
    return results

def main(username, start_year, end_year):
    sites = {
        "Daily Mirror": "https://www.dailymirror.lk",
        "Daily News": "https://www.dailynews.lk"
    }
    
    notifier = QueryNotifyPrint(verbose=True, print_all=True)
    notifier.start(username)
    
    all_results = []
    for site_name, base_url in sites.items():
        results = scrape_site(username, site_name, base_url)
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
