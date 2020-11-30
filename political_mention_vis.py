# Audrey Ding @alding

from cmu_112_graphics import *
from tweet_scraping import *
from politicians import *
import random


def appStarted(app):
    app.userOrSearch = "user" 
    app.user = "realDonaldTrump"

    # 2d list of top Republicans and their Twitter usernames
    # Partially based on popular Republican Twitter users and this list:
    # https://today.yougov.com/ratings/politics/popularity/Republicans/all 

    republicanUsers = [["Donald Trump", "realDonaldTrump"], 
                       ["Mike Pence", "Mike_Pence"], 
                       ["Ted Cruz", "tedcruz"],
                       ["Nikki Haley", "NikkiHaley"],
                       ["Mitch McConnell", "senatemajldr"],
                       ["Lindsey Graham", "LindseyGrahamSC"],
                       ["Rudy Guilani", "RudyGuilani"],
                       ["Donald Trump Jr.", "DonaldJTrumpJr"],
                       ["Ben Carson", "SecretaryCarson"]]


    # 2d list of top Democrats and their Twitter usernames
    # Partially based on popular Democratic Twitter users and this list:
    # https://today.yougov.com/ratings/politics/popularity/Democrats/all 
    democraticUsers = [["Joe Biden", "JoeBiden"],
                       ["Kamala Harris", "KamalaHarris"],
                       ["Alexandria Ocasio-Cortez", "AOC"],
                       ["Bernie Sanders", "BernieSanders"],
                       ["Barack Obama", "BarackObama"],
                       ["Elizabeth Warren", "ewarren"],
                       ["Hillary Clinton", "HillaryClinton"],
                       ["Nancy Pelosi", "SpeakerPelosi"],
                       ["Pete Buttigieg", "PeteButtigieg"]]
                       
    # List of Politician objects 
    app.politicians = []
    for i in range(len(republicanUsers)):
        app.politicians.append(Politician(republicanUsers[i][0], republicanUsers[i][1], "red"))
    for j in range(len(democraticUsers)):
        app.politicians.append(Politician(democraticUsers[i][0], democraticUsers[i][1], "blue"))

    randomIndex = random.randint(0, app.count - 1)
    app.randTweet = app.tweets[randomIndex]

def compareCounts(app, keyword, since):
    # since = "2020-11-26"
    for politician in app.politicians:
        count = countTweetsWithUser(politician.username, keyword, since)
        politician.setCount(count)

def redrawAll(app, canvas):
    

    # displayCount = f"@{app.user} has tweeted {app.count} times since {app.since}"
    # canvas.create_text(400, 50, text=displayCount)
    # title = f"Here's a random tweet from @{app.user} from any time since {app.since}: "
    # canvas.create_text(400, 150, text=title)
    # canvas.create_text(400, 200, text=app.randTweet)

