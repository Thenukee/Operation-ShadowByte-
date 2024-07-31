import requests
from bs4 import BeautifulSoup
import statistics

BASE_URL = "https://books.toscrape.com/"

url = BASE_URL + "catalogue/category/books/philosophy_7/index.html"

response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")

price_tags = soup.findAll("p", {"class": "price_color"})

prices = [float(price.text[2:]) for price in price_tags]
print(prices)
print(statistics.mean(prices))
