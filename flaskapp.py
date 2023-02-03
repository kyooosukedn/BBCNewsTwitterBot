from flask import Flask, render_template
import tweepy
import json

app = Flask(__name__)

# set up the API connection
auth = tweepy.OAuth1UserHandler() # Replace this with your API Keys and Access Token
api = tweepy.API(auth)

try:
    api.verify_credentials()
    print("Authentification successful")
    tweets = api.user_timeline()
except Exception as e:
    print("Failed", e)


# Process each tweet
for tweet in tweets:
    # Get the url if it exists in the tweet
    if 'urls' in tweet.entities and len(tweet.entities.get('urls', [])) > 0:
        url = tweet.entities['urls'][0]['url']
    else:
        url = ""
    

@app.route("/")
def tweets():
    tweets = api.user_timeline(count=15)
    # Or just retrieve tweets from some users, e.g kingjames (api.get_user)
    return render_template("page.html", tweets=tweets, url=url)
    

if __name__ == "__main__":
    app.run(debug=True)

