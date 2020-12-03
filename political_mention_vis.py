# Audrey Ding @alding

# Using cmu_112_graphics from 15-112 course notes

from cmu_112_graphics import *
from tweet_scraping import *
from politicians import *
from datetime import date, timedelta
import math
import random

def appStarted(app):
    # 2d list of top Republicans and their Twitter usernames
    # Partially based on popular Republican Twitter users and this list:
    # https://today.yougov.com/ratings/politics/popularity/Republicans/all 

    republicanUsers = [["Donald Trump", "realDonaldTrump"], 
                       ["Mike Pence", "Mike_Pence"], 
                       ["Ted Cruz", "tedcruz"],
                       ["Mitch McConnell", "senatemajldr"],
                       ["Lindsey Graham", "LindseyGrahamSC"],
                       ["Donald Trump Jr.", "DonaldJTrumpJr"],]

    # 2d list of top Democrats and their Twitter usernames
    # Partially based on popular Democratic Twitter users and this list:
    # https://today.yougov.com/ratings/politics/popularity/Democrats/all 
    democraticUsers = [["Joe Biden", "JoeBiden"],
                       ["Kamala Harris", "KamalaHarris"],
                       ["Alexandria Ocasio-Cortez", "AOC"],
                       ["Bernie Sanders", "BernieSanders"],
                       ["Barack Obama", "BarackObama"],
                       ["Hillary Clinton", "HillaryClinton"]]
                       
    # List of Politician objects 
    app.politicians = []
    for republican in republicanUsers:
        app.politicians.append(Politician(republican[0], republican[1], "red"))
    for democrat in democraticUsers:
        app.politicians.append(Politician(democrat[0], democrat[1], "blue"))

    # randomIndex = random.randint(0, app.count - 1)
    # app.randTweet = app.tweets[randomIndex]

    app.keyword = "election"
    app.since = "2020-11-30"
    getCounts(app)
    app.maxCount = greatestCount(app)
    
    app.buttons = []

    makeButtons(app)

    app.buttonClicked = False
    app.currButton = None

def getCounts(app):
    for politician in app.politicians:
        count = countTweetsWithUser(politician.username, app.keyword, app.since)
        print(count)
        politician.setCount(count)

def greatestCount(app):
    maxCount = 0
    for politician in app.politicians:
        if politician.count > maxCount:
            maxCount = politician.count
    return maxCount

def mousePressed(app, event):
    for button in app.buttons:
        if pointInCircle(event.x, event.y, button.x, button.y, button.r):
            app.buttonClicked = True
            app.currButton = button
            print("YES")

def pointInCircle(x0, y0, x1, y1, r):
   return ((x1 - x0)**2 + (y1 - y0)**2)**0.5 <= r
    
def drawIndividualFramework(app, canvas):
    # Cover canvas
    canvas.create_rectangle(0, 0, app.width, app.height, fill="white")
    # Draw title 
    title = f"{app.currButton.politician.name}'s tweets on \"{app.keyword}\""
    canvas.create_text(app.width / 2, 50, text=title, font="Arial 18 bold")
    margin = 50 # 50 px margin on sides and bottom
    topMargin = 100 # to leave room for the title
    # Draw plot frame with margins
    canvas.create_rectangle(margin, topMargin, app.width - margin, 
                            app.height - margin) 

def drawIndividualPlot(app, canvas):
    margin = 50
    topMargin = 100
    plotWidth = app.width - margin * 2
    plotHeight = app.height - margin - topMargin 
    
    (counts, today) = calculatePlotCounts(app)
    maxCount = max(counts) # largest count that determines y axis scale
    yLabel = int(math.ceil(maxCount / 10) * 10) # round to nearest ten for label
    # Draw yLabel on y axis
    canvas.create_text(margin - 10, topMargin, text=yLabel, font="Arial 12")

    for i in range(len(counts)):
        x = int(plotWidth / len(counts)) * i + margin
        y = int((counts[i] / yLabel) * plotHeight) + topMargin
        # Draw label on x axis 
        days = 30 - i
        xLabel = f"{days} days ago"
        canvas.create_text(x, app.height - margin / 2, text=xLabel, font="Arial 12")

        # Draw dot
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5)
    
    # Draw point for today
    x = plotWidth + margin
    y = int((today / yLabel) * plotHeight) + topMargin
    # Draw x label
    canvas.create_text(x, app.height - margin / 2, text="today", font="Arial 12")
    # Draw dot
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5)

# Calculates 5-day-increment tweet frequencies (y-values to be plotted)
# Returns list of y-values to be plotted and today's frequency
#   Return today's frequency here to minimize how many times we scrape
def calculatePlotCounts(app):
    # Datetime implementation from
    # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-5.php
    thirtyDaysAgo = date.today() - timedelta(31) # "since" arg is exclusive
    cumulative = []
    # Get cumulative counts for since 30 days ago, 25, 20, 15, ...
    for i in range(0, 30, 5):
        # Get since date and find cumulative count
        dt = thirtyDaysAgo + timedelta(i)
        count = countTweetsWithUser(app.currButton.politician.username, app.keyword, str(dt))
        cumulative.append(count)

    differences = []
    for j in range(len(cumulative) - 1):
        differences.append(cumulative[j] - cumulative[j + 1])

    return (differences, cumulative[0])


def makeButtons(app):
    cellWidth = int(app.width / 5)
    cellHeight = int(app.height / 4)
    polIndex = 0
    for y in range(cellHeight, app.height, cellHeight):
        for x in range(cellWidth, app.width, cellWidth):
            currentPol = app.politicians[polIndex]
            maxR = min(cellWidth, cellHeight) / 2
            # Calculate radius based on proportion with maxCount
            r = (currentPol.count / app.maxCount) * maxR
            app.buttons.append(Button(x, y, r, currentPol))

            polIndex += 1

# Loop through buttons and draw them
def drawButtons(app, canvas):
    for button in app.buttons:
        x = button.x
        y = button.y
        r = button.r
        # Draw buttons
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=button.politician.party)
        # Draw politician name and count
        canvas.create_text(x, y, text=button.politician.count, font="Arial 12")
        canvas.create_text(x, y + 30, text=button.politician.name, font="Arial 12")

def redrawAll(app, canvas):
    drawButtons(app, canvas)
    if app.buttonClicked:
        drawIndividualFramework(app, canvas)
        drawIndividualPlot(app, canvas)
