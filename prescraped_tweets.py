from tweet_scraping import *
import json
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

tweetData = {}
tweetData["scrapeDate"] = str(date.today())
 
for user in users:
    username = user[1]
    # Records date the data was updated, 
    #   have to cast datetime to str so it's JSON serializable
    # List of [date created, tweet text] for more efficient lookup
    tweetData[username] = getTweets("user", username, since) 

# Next two lines from:
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
with open("tweet_data.json", "w") as outfile:
    json.dump(tweetData, outfile)

print("Done")