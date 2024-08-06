
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from openpyxl import Workbook
import logging
import sys

# Define a function to get response with error handling
def get_response(url, timeout):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        return response, None, None
    except requests.exceptions.HTTPError as errh:
        return None, "HTTP Error", str(errh)
    except requests.exceptions.ProxyError as errp:
        return None, "Proxy Error", str(errp)
    except requests.exceptions.ConnectionError as errc:
        return None, "Error Connecting", str(errc)
    except requests.exceptions.Timeout as errt:
        return None, "Timeout Error", str(errt)
    except requests.exceptions.RequestException as err:
        return None, "Unknown Error", str(err)

# Define function to fetch articles
def fetch_articles(url, person_name, timeout, start_year, end_year):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
    }
    response, error_context, exception_text = get_response(url, timeout)
    
    if error_context:
        logging.error(f"Error fetching URL {url}: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for article in soup.find_all('article'):
        headline = article.find('h1') or article.find('h2') or article.find('h3')
        if headline:
            headline_text = headline.get_text()
            if person_name.lower() in headline_text.lower():
                article_url = article.find('a')['href']
                if not article_url.startswith('http'):
                    article_url = url + article_url
                date_published = article.find('time')
                date_text = date_published.get('datetime') if date_published else 'Unknown'
                article_date = datetime.strptime(date_text, "%Y-%m-%d") if date_text != 'Unknown' else datetime.min

                if start_year <= article_date.year <= end_year:
                    image_url = None
                    img_tag = article.find('img')
                    if img_tag and img_tag.get('src'):
                        image_url = img_tag.get('src')
                        if not image_url.startswith('http'):
                            image_url = url + image_url

                    articles.append((url, article_url, headline_text, image_url, date_text))

    return articles

# Define functions to fetch articles from specific newspapers
def fetch_articles_from_newspaper(url, newspaper_name, timeout, start_year, end_year):
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching {newspaper_name}: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h3').text.strip() if article.find('h3') else None
            if headline:
                article_url = article.find('a')['href'].strip()
                if not article_url.startswith('http'):
                    article_url = url + article_url
                publication_date = article.find('time').text.strip() if article.find('time') else 'Unknown'
                article_date = datetime.strptime(publication_date, "%Y-%m-%d") if publication_date != 'Unknown' else datetime.min
                if start_year <= article_date.year <= end_year:
                    articles.append({
                        'Newspaper': newspaper_name,
                        'Article URL': article_url,
                        'Headline': headline,
                        'Publication Date': publication_date
                    })
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    return articles

# Function to fetch articles from all defined newspapers
def fetch_all_articles(timeout, start_year, end_year):
    site_data = {
        "Daily Mirror": "https://www.dailymirror.lk/",
        "Daily News": "https://www.dailynews.lk/",
        "The Sunday Times": "https://www.sundaytimes.lk/",
        "The Island": "https://www.island.lk/",
        "Sunday Observer": "https://www.sundayobserver.lk/",
        "Ada Derana": "https://www.adaderana.lk/"
    }
    all_articles = []
    for newspaper, url in site_data.items():
        all_articles.extend(fetch_articles_from_newspaper(url, newspaper, timeout, start_year, end_year))
    return all_articles

# Main function to run the scraper
def main(username, start_year, end_year):
    timeout = 60
    
    print(f"Searching for articles related to '{username}' from {start_year} to {end_year}.")
    
    all_articles = fetch_all_articles(timeout, start_year, end_year)
    
    results_df = []
    for article in all_articles:
        if username.lower() in article['Headline'].lower():
            results_df.append([
                article['Newspaper'],
                article['Article URL'],
                article['Headline'],
                'N/A',  # No image URL in the new fetch functions
                article['Publication Date']
            ])
    
    df = pd.DataFrame(results_df, columns=["Newspaper", "Article URL", "Headline", "Image URL", "Publication Date"])
    output_file = "results.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Scraping completed. Results saved to {output_file}")

if __name__ == "__main__":
    username = input("Enter the person's name: ")
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    main(username, start_year, end_year)
