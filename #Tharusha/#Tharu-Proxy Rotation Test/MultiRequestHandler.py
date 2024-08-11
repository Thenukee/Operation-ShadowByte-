import requests
from bs4 import BeautifulSoup
import statistics
import queue
import threading
import random

BASE_URL = "http://books.toscrape.com/"
url = BASE_URL + "catalogue/category/books/philosophy_7/index.html"

# Read proxies from file
with open("ProxyList.txt", "r") as f:
    proxies = f.read().split("\n")

# Define a function to send a web scraping request using a proxy
def send_request(proxy, proxy_counts):
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "lxml")
            price_tags = soup.findAll("p", {"class": "price_color"})
            prices = [float(price.text[2:]) for price in price_tags]
            mean_price = statistics.mean(prices)
            print(f"Proxy: {proxy}, Mean price: {mean_price}")
            # Increment the count for the proxy
            proxy_counts[proxy] = proxy_counts.get(proxy, 0) + 1
    except Exception as e:
        print(f"Error with proxy {proxy}: {e}")

# Create a queue and add proxies to it
q = queue.Queue()
for p in proxies:
    q.put(p)

# Start checking proxies and sending web scraping requests
checked_proxies = []
proxy_counts = {}  # Dictionary to store proxy usage counts
while not q.empty():
    proxy = q.get()
    try:
        res = requests.get("http://ipinfo.io/json", proxies={"http": proxy, "https": proxy}, timeout=5)
    except:
        continue
    if res.status_code == 200:
        checked_proxies.append(proxy)
        threading.Thread(target=send_request, args=(proxy, proxy_counts)).start()

# Shuffle all the proxies
random.shuffle(checked_proxies)

# Start sending web scraping requests with shuffled proxies
for proxy in checked_proxies:
    threading.Thread(target=send_request, args=(proxy, proxy_counts)).start()

# Wait for all threads to complete
threading.Event().wait(5)

# Print the table of proxy usage counts
print("\nProxy Usage Counts:")
for proxy, count in proxy_counts.items():
    print(f"{proxy:<20} {count}")
