import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import sys
from datetime import datetime

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

def fetch_articles_from_daily_news(timeout, start_year, end_year):
    url = "https://www.dailynews.lk/"
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching Daily News: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h3').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.dailynews.lk' + article_url
            publication_date = article.find('time').text.strip()
            articles.append({
                'Newspaper': 'Daily News',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

    return articles

def fetch_articles_from_daily_mirror(timeout, start_year, end_year):
    url = "https://www.dailymirror.lk/"
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching Daily Mirror: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.dailymirror.lk' + article_url
            publication_date = article.find('time').text.strip()
            articles.append({
                'Newspaper': 'Daily Mirror',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

    return articles

def fetch_articles_from_sunday_observer(timeout, start_year, end_year):
    url = "https://www.sundayobserver.lk/"
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching Sunday Observer: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h3').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.sundayobserver.lk' + article_url
            publication_date = article.find('time').text.strip()
            articles.append({
                'Newspaper': 'Sunday Observer',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

    return articles

def fetch_articles_from_adaderana(timeout, start_year, end_year):
    url = "https://www.adaderana.lk/"
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching Ada Derana: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.adaderana.lk' + article_url
            publication_date = article.find('time').text.strip()
            articles.append({
                'Newspaper': 'Ada Derana',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

    return articles

def fetch_articles_from_sunday_times(timeout, start_year, end_year):
    url = "https://www.sundaytimes.lk/"
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching Sunday Times: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h3').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.sundaytimes.lk' + article_url
            publication_date = article.find('time').text.strip()
            articles.append({
                'Newspaper': 'Sunday Times',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

    return articles

def fetch_articles_from_the_island(timeout, start_year, end_year):
    url = "https://www.theisland.lk/"
    response, error_context, exception_text = get_response(url, timeout)
    if error_context:
        logging.error(f"Error fetching The Island: {error_context} - {exception_text}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")

    articles = []
    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.theisland.lk' + article_url
            publication_date = article.find('time').text.strip()
            articles.append({
                'Newspaper': 'The Island',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

    return articles

def fetch_all_articles(timeout, start_year, end_year):
    all_articles = []
    all_articles.extend(fetch_articles_from_daily_news(timeout, start_year, end_year))
    all_articles.extend(fetch_articles_from_daily_mirror(timeout, start_year, end_year))
    all_articles.extend(fetch_articles_from_sunday_observer(timeout, start_year, end_year))
    all_articles.extend(fetch_articles_from_adaderana(timeout, start_year, end_year))
    all_articles.extend(fetch_articles_from_sunday_times(timeout, start_year, end_year))
    all_articles.extend(fetch_articles_from_the_island(timeout, start_year, end_year))

    return all_articles

def main(username, start_year, end_year):
    # Setup
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