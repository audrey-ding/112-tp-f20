# Audrey Ding @alding

# This file contains the part of the program that uses snscrape or Tweepy

# REFERENCE LIST: (didn't use directly but referred to)
# http://docs.tweepy.org/en/latest/index.html
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
# https://github.com/JustAnotherArchivist/snscrape

# From Python library
import os # https://docs.python.org/3/library/os.html 
import json # https://docs.python.org/3/library/json.html 
import time # https://docs.python.org/3/library/time.html 
from subprocess import Popen, PIPE, STDOUT # https://docs.python.org/3/library/subprocess.html

# Tweepy module http://docs.tweepy.org/en/latest/index.html 
import tweepy
from tweepy import RateLimitError

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

            # Reference for Tweepy Status object:
            # https://www.geeksforgeeks.org/python-status-object-in-tweepy/

            date = status.created_at
            text = status.full_text
            # Get list of hashtag dicts from entities of Status
            hashtagDicts = status.entities["hashtags"]
            # Loop through hashtag dicts and add hashtag text to list
            hashtags = [] # list of hashtags (str)
            for currDict in hashtagDicts:
                hashtags.append(currDict["text"])
            # Get list of mention dicts from entities of Status
            mentionDicts = status.entities["user_mentions"]
            # Loop through mention dicts and add mentioned usernames to list
            mentions = [] # list of mentioned usernames (str)
            for currDict in mentionDicts:
                mentions.append(currDict["screen_name"])

            # Have to cast datetime to str so it's JSON serializable
            tweets.append([str(date), text, hashtags, mentions]) 
        
    print(f'Scraped all tweets.')
    return tweets
