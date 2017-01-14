import re
import csv
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from tweepy import TweepError

pd.options.display.max_columns = 50
pd.options.display.max_rows= 50
pd.options.display.width= 120

consumer_key = "Y9LSrr5Ctyco96MxuB5lVrXLE" # Use your own key. To get a key https://apps.twitter.com/
consumer_secret = "MZ0ZzvzcyDFQAri4YFQ1NUJIUdyaaKr22YoHt1sdE6yVkUPOk4"

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_all_tweets(screen_name):
    #Twitter only allows access to a users most recent 3240 tweets with this method

    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    #initialize a list to hold all the tweepy Tweets
    alltweets = []
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    print "%s %s tweets downloaded so far ..." % (screen_name, len(alltweets))
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        # print "getting tweets before %s" % (oldest)

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print "%s %s tweets downloaded  so far ..." % (screen_name, len(alltweets))

    #transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    
    return alltweets
    
    #write the csv
    '''with open('%s_tweets.csv' % screen_name, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["id","created_at","text"])
        writer.writerows(outtweets) '''

    pass

def get_related_tweets(alltweets, brand_name):
    related_tweets = ""
    for tweet in alltweets:
        tweet_text = tweet.text.encode("utf-8").lower()
        if brand_name in tweet_text:
            related_tweets += tweet_text + "\n"
            
    return related_tweets


def get_related_tweets_for_user(screen_name, brand_name):
    alltweets = get_all_tweets(screen_name)
    return get_related_tweets(alltweets, brand_name)