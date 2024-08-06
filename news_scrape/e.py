import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

news_list = []

def fetch_articles_from_daily_news():
    url = "https://www.dailynews.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all('article'):
        try:
            headline = article.find('h3').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.dailynews.lk' + article_url
            publication_date = article.find('time').text.strip()
            news_list.append({
                'Newspaper': 'Daily News',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

def fetch_articles_from_daily_mirror():
    url = "https://www.dailymirror.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.dailymirror.lk' + article_url
            publication_date = article.find('time').text.strip()
            news_list.append({
                'Newspaper': 'Daily Mirror',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

def fetch_articles_from_sunday_observer():
    url = "https://www.sundayobserver.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.sundayobserver.lk' + article_url
            publication_date = article.find('time').text.strip()
            news_list.append({
                'Newspaper': 'Sunday Observer',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

def fetch_articles_from_adaderana():
    url = "https://www.adaderana.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all('article'):
        try:
            headline = article.find('h3').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.adaderana.lk' + article_url
            publication_date = article.find('time').text.strip()
            news_list.append({
                'Newspaper': 'Ada Derana',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

def fetch_articles_from_sunday_times():
    url = "https://www.sundaytimes.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.sundaytimes.lk' + article_url
            publication_date = article.find('time').text.strip()
            news_list.append({
                'Newspaper': 'Sunday Times',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

def fetch_articles_from_the_island():
    url = "https://www.island.lk/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    for article in soup.find_all('article'):
        try:
            headline = article.find('h2').text.strip()
            article_url = article.find('a')['href'].strip()
            if not article_url.startswith('http'):
                article_url = 'https://www.island.lk' + article_url
            publication_date = article.find('time').text.strip()
            news_list.append({
                'Newspaper': 'The Island',
                'Article URL': article_url,
                'Headline': headline,
                'Publication Date': publication_date
            })
        except Exception as e:
            print(f"An error occurred: {e}")

def fetch_all_articles():
    fetch_articles_from_daily_news()
    fetch_articles_from_daily_mirror()
    fetch_articles_from_sunday_observer()
    fetch_articles_from_adaderana()
    fetch_articles_from_sunday_times()
    fetch_articles_from_the_island()

    # Save to Excel
    df = pd.DataFrame(news_list)
    df.to_excel('news_articles.xlsx', index=False)

if __name__ == "__main__":
    fetch_all_articles()
    print("Articles have been fetched and saved to news_articles.xlsx")
