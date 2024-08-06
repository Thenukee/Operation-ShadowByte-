import requests
from bs4 import BeautifulSoup
import time

#Requesting the website
URL='https://www.bbc.com/news'
response=requests.get(URL)
print("The Response code is :",response)
 
#Parse the html doc
soup=BeautifulSoup(response.content,'html.parser')

#Extract the news headline from HTMl
headlines=soup.find_all('h3')

#Display the headlines
for headline in headlines:
    print(headline.text)
    time.sleep(1) 