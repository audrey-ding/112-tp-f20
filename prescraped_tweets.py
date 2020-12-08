from tweet_scraping import * # (my file) import scraping functinos
import json # to read/write json file
# From Python library: https://docs.python.org/3/library/datetime.html 
from datetime import date, timedelta 

users = [["Donald Trump", "realDonaldTrump"], 
         ["Mike Pence", "Mike_Pence"], 
         ["Ted Cruz", "tedcruz"],
         ["Mitch McConnell", "senatemajldr"],
         ["Lindsey Graham", "LindseyGrahamSC"],
         ["Donald Trump Jr.", "DonaldJTrumpJr"],
         ["Joe Biden", "JoeBiden"],
         ["Kamala Harris", "KamalaHarris"],
         ["Alexandria Ocasio-Cortez", "AOC"],
         ["Bernie Sanders", "BernieSanders"],
         ["Barack Obama", "BarackObama"],
         ["Hillary Clinton", "HillaryClinton"]]

# "since" arg is exclusive, so add 1 to number of days
since = date.today() - timedelta(101) 

tweetData = {} # dictionary to store all data, mapping usernames to tweets
# Records date the data was updated, 
    #   have to cast datetime to str so it's JSON serializable
tweetData["scrapeDate"] = str(date.today()) 
 
# Loop through users, scrape, and add to dictionary
for user in users:
    username = user[1] # get username
    # Scrape tweets matching username and date
    tweetData[username] = getTweets("user", username, since)

# Next two lines from:
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
# Write json file
with open("tweet_data.json", "w") as outfile:
    json.dump(tweetData, outfile)

print("Done")