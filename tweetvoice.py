import speech_recognition as sr
import tweepy
import webbrowser
import subprocess

# Authentification
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret,access_token,access_token_secret)
api = tweepy.API(auth)

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

def search_tweets(api, keyword):
    tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(10)
    for tweet in tweets:
        print(tweet.text)

while True:
    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")

    # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    
        # using google speech recognition
        text = r.recognize_google(audio_text, language = 'en-EN')
        print("Text: "+ text)
        
        if text == "tweet":
            print("What do you want to tweet?")
            audio_text = r.listen(source)
            tweet_text = r.reconigze_google(audio_text)
            auth = tweepy.OAuth1UserHandler() # Replace this with API and Access Token keys
            api = tweepy.API(auth)
            api.update_status(tweet_text)
            print("Successfully tweeted: " + tweet_text)
            
        elif text == "open browser":
            webbrowser.open("https://www.google.com")
            print("Browser opened")
        elif text == "BBC News":
            subprocess.run(["python", "bbcbot.py"])
            print("Script ran")   
        
        elif text == "search":
            keyword = input("Enter keyword: ")
            search_tweets(api, keyword)

        elif text == "exit":
            break;
    

print("Exiting..")
