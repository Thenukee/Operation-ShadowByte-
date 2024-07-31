import pandas as pd
from ntscraper import Nitter  # Ensure the module name is correct

# Initialize the scraper
scraper = Nitter(0)

# Function to get tweets based on a keyword or user
def get_tweets(name, mode, number):
    tweets = scraper.get_tweets(name, mode=mode, number=number)
    final_tweets = []
    for x in tweets['tweets']:
        data = [x['link'], x['text'], x['date'], x['stats']['likes'], x['stats']['comments']]
        final_tweets.append(data)
    dat = pd.DataFrame(final_tweets, columns=['twitter_link', 'text', 'date', 'likes', 'comments'])
    return dat

# Example usage to get tweets containing the hashtag 'india' and save to a CSV file
data = get_tweets('india', 'hashtag', 10)
data.to_csv('india_tweets.csv', index=False)
print("India tweets saved to india_tweets.csv")

# Getting profile information for Jeff Bezos
profile_info = scraper.get_profile_info("JeffBezos")
print(profile_info)

# Example usage to get tweets from a user and save to a CSV file
user_tweets = get_tweets('JeffBezos', 'user', 6)
user_tweets.to_csv('jeffbezos_tweets.csv', index=False)
print("Jeff Bezos tweets saved to jeffbezos_tweets.csv")

# Getting profile information for Bill Gates
bill_gates_profile = scraper.get_profile_info('BillGates')
print(bill_gates_profile)
