# Audrey Ding @alding

# CITATION LIST:
# (1) https://github.com/cedoard/snscrape_twitter 
# (2) https://www.saltycrane.com/blog/2008/09/how-get-stdout-and-stderr-using-python-subprocess-module/

# REFERENCE LIST: (didn't use directly but referred to)
# http://docs.tweepy.org/en/latest/index.html
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
# https://github.com/JustAnotherArchivist/snscrape

import os
import json
import time

import tweepy
from tweepy import RateLimitError

from subprocess import Popen, PIPE, STDOUT

# Gets and returns Twitter API 
# CITATION: from snscrape-twitter (1)
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

# Returns list of tweet IDs corresponding to a given query (user or keyword)
# CITATION: Adapted from snscrape-twitter (1)
def getTweetIDs(userOrSearch, query, since):
    tweetIDs = []
    # Ensure we are searching a valid keyword
    if len(keyword) > 0:
        print(f'Scraping tweets with keyword: "{query}" ...')
        try:
            # CITATION: these next two lines are from Salty Crane (2)
            # Runs command line
            cmd = f"snscrape --since {since} twitter-{userOrSearch} {query}" 
            p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True) 
            for line in p.stdout:
                # Discard front part of URL
                temp = line.decode().split("status/")
                tempStr = temp[1]
                tweetIDs.append(tempStr[:-1]) # discard \n character and append to result list
        except Exception as err:
            print(f"SNSCRAPE ERROR: {err}")
        
    print(f'Scraped all tweets.')
    return tweetIDs

# Returns list of tweets (text and shortened URL)
def getTweets(userOrSearch, query, since):
    tweets = [] 
    twitterAPI = getAPI()
    tweetIDs = getTweetIDs(userOrSearch, query, since)
    for singleID in tweetIDs:
        tweets.append(twitterAPI.get_status(singleID).text)
    return tweets

# Passes a keyword and a list of tweets from a user since a specific date
# Returns number of tweets from the user (since the date) that matches the keyword
def countTweetsWithUser(user, keyword, since):
    tweets = getTweetIDs("user", user, since)
    counts = 0
    for tweet in tweets:
        # search isn't case sensitive
        if keyword.lower() in tweet.lower(): 
            counts += 1
    return counts

# Returns number of tweets under a specific query
def countTweets(userOrSearch, query, since):
    tweets = getTweetIDs(userOrSearch, query, since)
    return len(tweets)s