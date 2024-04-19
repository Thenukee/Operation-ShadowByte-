import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

usernames = ["jlo", "shakira", "beyonce", "katyperry"]
output = {}

def scrape(username):
    url = f'https://instagram.com/{username}/?__a=1&__d=dis'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data_json = response.json()
            user_data = data_json['graphql']['user']
            parse_data(username, user_data)
            print("Success")
        else:
            print(f"Failed: {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

def parse_data(username, user_data):
    captions = []
    if len(user_data['edge_owner_to_timeline_media']['edges']) > 0:
        for node in user_data['edge_owner_to_timeline_media']['edges']:
            if len(node['node']['edge_media_to_caption']['edges']) > 0:
                if node['node']['edge_media_to_caption']['edges'][0]['node']['text']:
                    captions.append(
                        node['node']['edge_media_to_caption']['edges'][0]['node']['text']
                    )

    output[username] = {
        'name': user_data['full_name'],
        'category': user_data['category_name'],
        'followers': user_data['edge_followed_by']['count'],
        'posts': captions,
    }

def main():
    for username in usernames:
        scrape(username)

if __name__ == '__main__':
    main()
    pprint(output)
