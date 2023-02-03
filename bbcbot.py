import tweepy
import requests
from bs4 import BeautifulSoup

# Replace these with your own API keys and secrets
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# Authenticate with the Twitter API
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)


# Check if the credentials are valid
tweets = []
try:
    api.verify_credentials()
    print("Authentication successful")
    tweets = api.user_timeline()
except Exception as e:
    print("Authentication failed:", e)
    

url = 'https://www.bbc.com/news'

# Make a get request to fetch the raw HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, "lxml")

news_items = soup.find_all('div', class_='gs-c-promo nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m nw-u-w-auto gs-c-promo--flex')

def tweet_news_item(tweet_text):
    api.update_status(tweet_text)

threads = []
tweet_text = ""
current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 


# Iterate over the news items and create a thread for each
for item in news_items[:5]:
    title = item.find('h3', class_='gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text')
    link = item.find('a', class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor')
    href = link["href"]
    if title:
        tweet_text = title.text + "\n"
        tweet_text += f"Link: https://bbc.com" + href + "\n\n"
        thread = threading.Thread(target=tweet_news_item, args=(tweet_text,))
        threads.append(thread)

# Start the threads
for thread in threads:
    thread.start()

# Wait for the threads to finish
for thread in threads:
    thread.join()

api.update_status(f"News today ({ current_date }):\n\n")
