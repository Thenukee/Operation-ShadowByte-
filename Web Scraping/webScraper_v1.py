import requests
from bs4 import BeautifulSoup
import pandas as pd

# Replace 'url' with the URL of the website you want to scrape
url = 'https://ikman.lk/en/ad/nissan-sunny-super-saloon-n17-2005-for-sale-kalutara'

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the data you need from the parsed HTML
# For example, let's say you want to extract all the links on the page
links = soup.find_all('a')

# Create a list of dictionaries containing the data
data = [{'Link Text': link.text, 'URL': link.get('href')} for link in links]

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Write the DataFrame to an Excel file
# Replace 'output.xlsx' with the desired file name
df.to_excel('output4.xlsx', index=False)

print('Data has been scraped and saved to output.xlsx')
