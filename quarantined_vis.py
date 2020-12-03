from cmu_112_graphics import *
from tweet_scraping import *
from politicians import *
from datetime import date, timedelta
import math
import random
import sys

def appStarted(app):
    bern = Politician("Bernie Sanders", "BernieSanders", "blue")
    ted = Politician("Ted Cruz", "tedcruz", "red")
    app.currButton = Button(0, 0, 0, ted)
    app.keyword = "election"
    app.plotValues = []
    app.today = 0
    calculatePlotCounts(app)

# Calculates 5-day-increment tweet frequencies (y-values to be plotted)
# Returns list of y-values to be plotted and today's frequency
#   Return today's frequency here to minimize how many times we scrape
def calculatePlotCounts(app):
    # Datetime implementation from
    # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-5.php
    thirtyDaysAgo = date.today() - timedelta(31) # "since" arg is exclusive
    cumulative = []
    # Get cumulative counts for since 30 days ago, 25, 20, 15, ...
    for i in range(0, 31, 5):
        # Get since date and find cumulative count
        dt = thirtyDaysAgo + timedelta(i)
        try:
            count = countTweetsWithUser(app.currButton.politician.username, app.keyword, str(dt))
        except:
            print("STOP")
            # sys.exit implementation from https://stackoverflow.com/a/438902
            sys.exit(1)
        print(f"{30 - i} days ago, {count}")
        cumulative.append(count)
    
    app.today = cumulative[len(cumulative) - 1]

    for j in range(len(cumulative) - 1):
        app.plotValues.append(cumulative[j] - cumulative[j + 1])


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
    

    maxCount = max(app.plotValues) # largest count that determines y axis scale
    yLabel = int(math.ceil(maxCount / 10) * 10) # round to nearest ten for label
    # Draw yLabel on y axis
    canvas.create_text(margin - 10, topMargin, text=yLabel, font="Arial 12")

    points = [] # 2d list storing point coords
    for i in range(len(app.plotValues)):
        x = int(plotWidth / len(app.plotValues)) * i + margin
        y = app.height - margin - int((app.plotValues[i] / yLabel) * plotHeight) 
        # Draw label on x axis 
        xLabel = f"{30 - i*5} days ago"
        canvas.create_text(x, app.height - margin / 2, text=xLabel, font="Arial 12")

        # Draw dot
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
        points.append([x, y])
    
    # Draw point for today
    x = plotWidth + margin
    y = app.height - margin - int((app.today / yLabel) * plotHeight) + topMargin
    # Draw x label
    canvas.create_text(x, app.height - margin / 2, text="today", font="Arial 12")
    # Draw dot
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
    points.append([x, y])

    # Draw connecting lines 
    for j in range(len(points) - 1):
        canvas.create_line(points[j][0], points[j][1], points[j+1][0], 
                           points[j+1][1], fill="black", width=3)

def redrawAll(app, canvas):
    try:
        drawIndividualFramework(app, canvas)
        drawIndividualPlot(app, canvas)
    except Exception as err:
        canvas.create_text(app.width / 2, app.height / 2, 
                           text=f"Rate limit exceeded. Try again later")