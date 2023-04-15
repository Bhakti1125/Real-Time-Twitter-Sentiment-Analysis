# importing the required libraries
import tweepy
import pandas as pd
from preprocess import clean_tweet
from preprocess import remove_stopwords
from preprocess import get_subjectivity
from preprocess import get_polarity
from sentiments import add_sentiment
import os


# twitter credentials
# keys and tokens from the twitter developer account
consumer_key = 'e7bmCtJmJwoxYubpq8t9zv1hA'
consumer_secret = '9u9y65OuoxIdjFLfD5mLcDiChEABWNfh0rDHYjlWFHoMnE0dnB'
access_token = '912151897519226880-qfS43tvJqP207W1rZIMUHLgaZSfGQhF'
access_token_secret = 'vGOlSWNHMhQlRC2vH3Gx2LxSIZPqQ9vkehA9bpJrGQhFw'


# attempt authentication
try:
    # create OAuthHandler object
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # set access token and secret
    auth.set_access_token(access_token, access_token_secret)
    # create tweepy API object to fetch tweets
    api = tweepy.API(auth,wait_on_rate_limit=True)
except:
    print("Error: Authentication Failed")


def get_tweets(keyword, count=1000):
    """
    Get tweets containing the given keyword.
    """
    tweets = tweepy.Cursor(api.search_tweets,
                           q=keyword,
                           lang='en').items(count)

    return [{'Tweet': clean_tweet(tweet.text),
             'Timestamp': tweet.created_at,
             'Subjectivity': get_subjectivity(tweet.text),
             'Polarity': get_polarity(tweet.text)} for tweet in tweets]

def analyze_tweets(keyword, count=1000):
    """
    Analyze tweets containing the given keyword.
    """
    tweets = get_tweets(keyword, count)
    df = pd.DataFrame(tweets)
    df = add_sentiment(df)


    return df
