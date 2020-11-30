# Audrey Ding @alding

from cmu_112_graphics import *
from tweet_scraping import *
from politicians import *
import random


def appStarted(app):
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
    for republican in republicanUsers:
        app.politicians.append(Politician(republican[0], republican[1], "red"))
    for democrat in democraticUsers:
        app.politicians.append(Politician(democrat[0], democrat[1], "blue"))

    # randomIndex = random.randint(0, app.count - 1)
    # app.randTweet = app.tweets[randomIndex]

    getCounts(app, "election", "2020-11-25")
    app.maxCount = greatestCount(app)

def getCounts(app, keyword, since):
    for politician in app.politicians:
        count = countTweetsWithUser(politician.username, keyword, since)
        print(count)
        politician.setCount(count)

def greatestCount(app):
    maxCount = 0
    for politician in app.politicians:
        if politician.count > maxCount:
            maxCount = politician.count
    return maxCount

def drawButtons(app, canvas):
    cellWidth = int(app.width / 5)
    cellHeight = int(app.height / 5)
    polIndex = 0
    for y in range(cellHeight, app.height, cellHeight):
        for x in range(cellWidth, app.width, cellWidth):
            currentPol = app.politicians[polIndex]
            # If the currentPol's count isn't 0, draw button
            if currentPol.count != 0:
                maxR = min(cellWidth, cellHeight) / 2
                # Calculate radius based on proportion with maxCount
                r = (currentPol.count / app.maxCount) * maxR
                currentPol.setButton(Button(x, y, r))
                # Draw circle
                canvas.create_oval(x - r, y - r, x + r, y + r, 
                                fill=currentPol.party)
                # Draw label with count, 3/4 down the circle
                canvas.create_text(x, y + r/2, text=currentPol.name, font="Arial 12")

            # Don't draw button if currentPol.count == 0, just draw count label
            else:
                canvas.create_text(x, y + 10, text=currentPol.name, font="Arial 12")

            # Draw label with name
            canvas.create_text(x, y, text=currentPol.count, font="Arial 12")

            polIndex += 1

def redrawAll(app, canvas):
    drawButtons(app, canvas)
    # displayCount = f"@{app.user} has tweeted {app.count} times since {app.since}"
    # canvas.create_text(400, 50, text=displayCount)
    # title = f"Here's a random tweet from @{app.user} from any time since {app.since}: "
    # canvas.create_text(400, 150, text=title)
    # canvas.create_text(400, 200, text=app.randTweet)

