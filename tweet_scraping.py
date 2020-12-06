# Audrey Ding @alding

# This file contains the part of the program that uses snscrape or Tweepy

# REFERENCE LIST: (didn't use directly but referred to)
# http://docs.tweepy.org/en/latest/index.html
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
# https://github.com/JustAnotherArchivist/snscrape

import os
import json
import time
import sys

import tweepy
from tweepy import RateLimitError

from subprocess import Popen, PIPE, STDOUT


# Gets and returns Twitter API 
# From https://github.com/cedoard/snscrape_twitter  
def getAPI():
    # Get Twitter auth keys from json file
    twitterAuthData = open("twitter_auth_data.json").read()
    twitterAuthDataJson = json.loads(twitterAuthData)

    accessToken = twitterAuthDataJson["access_token"]
    accessTokenSecret = twitterAuthDataJson["access_token_secret"]
    consumerKey = twitterAuthDataJson["consumer_key"]
    consumerSecret = twitterAuthDataJson["consumer_secret"]

    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)

    return api

# Returns list of tweets in the form [date created, tweet text] corresponding to 
#   a given query (user or keyword)
# Adapted from https://github.com/cedoard/snscrape_twitter 
def getTweets(userOrSearch, query, since):
    twitterAPI = getAPI()
    tweets = []
    # Ensure we are searching a valid keyword
    if len(query) > 0:
        print(f'Scraping tweets with keyword: "{query}" ...')
        # These next two lines are from:
        # https://www.saltycrane.com/blog/2008/09/how-get-stdout-and-stderr-using-python-subprocess-module/
        # Runs command line
        cmd = f"snscrape --since {since} twitter-{userOrSearch} {query}" 
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True) 
        i = 0
        for line in p.stdout:
            # Discard front part of URL
            temp = line.decode().split("status/")
            tempStr = temp[1]
            tweetID = tempStr[:-1]
            while True:
                try:
                    status = twitterAPI.get_status(tweetID, tweet_mode="extended")
                    # If it works, break out of the loop
                    break
                except RateLimitError as err:
                    # If quota exceeded, wait 1 min (60 secs) and continue
                    print(f"Rate limit exceeded: {time.ctime()}")
                    time.sleep(60)
                    print(f"Started again: {time.ctime()}")
            date = status.created_at
            text = status.full_text
            # Have to cast datetime to str so it's JSON serializable
            tweets.append([str(date), text]) 
        
    print(f'Scraped all tweets.')
    return tweets
