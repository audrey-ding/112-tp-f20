# Audrey Ding @alding

# Using cmu_112_graphics from 15-112 course notes
# This file handles visualizations

from cmu_112_graphics import *
from tweet_scraping import *
from politicians import *
from datetime import date, timedelta
import math
import random

class ComparisonMode(Mode):
    def appStarted(self):
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
        self.politicians = []
        for republican in republicanUsers:
            self.politicians.append(Politician(republican[0], republican[1], "red"))
        for democrat in democraticUsers:
            self.politicians.append(Politician(democrat[0], democrat[1], "blue"))

        self.keyword = "election"
        self.since = "2020-11-30"
        self.getCounts()
        self.maxCount = self.greatestCount()
        
        self.buttons = []
        self.makeButtons()

    def getCounts(self):
        for politician in self.politicians:
            count = countTweetsWithUser(politician.username, self.keyword, self.since)
            print(count)
            politician.setCount(count)

    def greatestCount(self):
        maxCount = 0
        for politician in self.politicians:
            if politician.count > maxCount:
                maxCount = politician.count
        return maxCount

    def mousePressed(self, event):
        for button in self.buttons:
            if pointInCircle(event.x, event.y, button.x, button.y, button.r):
                self.app.currButton = button
                self.app.setActiveMode(self.app.plotMode)

    def pointInCircle(x0, y0, x1, y1, r):
        return ((x1 - x0)**2 + (y1 - y0)**2)**0.5 <= r

    def makeButtons(self):
        cellWidth = int(self.width / 5)
        cellHeight = int(self.height / 4)
        polIndex = 0
        for y in range(cellHeight, self.height, cellHeight):
            for x in range(cellWidth, self.width, cellWidth):
                currentPol = self.politicians[polIndex]
                maxR = min(cellWidth, cellHeight) / 2
                # Calculate radius based on proportion with maxCount
                r = (currentPol.count / self.maxCount) * maxR
                self.buttons.append(Button(x, y, r, currentPol))
                polIndex += 1

    # Loop through buttons and draw them
    def drawButtons(self, canvas):
        for button in self.buttons:
            x = button.x
            y = button.y
            r = button.r
            # Draw buttons
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=button.politician.party, width=0)
            # Draw politician name and count
            canvas.create_text(x, y, text=button.politician.count, font="Arial 12")
            canvas.create_text(x, y + 30, text=button.politician.name, font="Arial 12")

    def redrawAll(self, canvas):
        self.drawButtons(canvas)

class PlotMode(Mode):
    def appStarted(self):
        self.keyword = "election"
        self.plotValues = []
        self.today = 0
        self.calculatePlotCounts()

    # Calculates 5-day-increment tweet frequencies (y-values to be plotted)
    # Returns list of y-values to be plotted and today's frequency
    #   Return today's frequency here to minimize how many times we scrape
    def calculatePlotCounts(self):
        # Datetime implementation from
        # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-5.php
        thirtyDaysAgo = date.today() - timedelta(31) # "since" arg is exclusive
        cumulative = []
        # Get cumulative counts for since 30 days ago, 25, 20, 15, ...
        for i in range(0, 31, 5):
            # Get since date and find cumulative count
            dt = thirtyDaysAgo + timedelta(i)
            try:
                count = countTweetsWithUser(self.app.currButton.politician.username, self.keyword, str(dt))
            except:
                print("STOP")
                # sys.exit implementation from https://stackoverflow.com/a/438902
                sys.exit(1)
            print(f"{30 - i} days ago, {count}")
            cumulative.append(count)
        
        self.today = cumulative[len(cumulative) - 1]

        for j in range(len(cumulative) - 1):
            self.plotValues.append(cumulative[j] - cumulative[j + 1])

    def drawIndividualFramework(self, canvas):
        # Cover canvas
        canvas.create_rectangle(0, 0, self.width, self.height, fill="white")
        # Draw title 
        title = f"{self.app.currButton.politician.name}'s tweets on \"{self.keyword}\""
        canvas.create_text(self.width / 2, 50, text=title, font="Arial 18 bold")
        margin = 50 # 50 px margin on sides and bottom
        topMargin = 100 # to leave room for the title
        # Draw plot frame with margins
        canvas.create_rectangle(margin, topMargin, self.width - margin, 
                                self.height - margin) 

    def drawIndividualPlot(self, canvas):
        margin = 50
        topMargin = 100
        plotWidth = self.width - margin * 2
        plotHeight = self.height - margin - topMargin 

        maxCount = max(self.plotValues) # largest count that determines y axis scale
        yLabel = int(math.ceil(maxCount / 10) * 10) # round to nearest ten for label
        # Draw yLabel on y axis
        canvas.create_text(margin - 10, topMargin, text=yLabel, font="Arial 12")

        points = [] # 2d list storing point coords
        for i in range(len(self.plotValues)):
            x = int(plotWidth / len(self.plotValues)) * i + margin
            y = self.height - margin - int((self.plotValues[i] / yLabel) * plotHeight) 
            # Draw label on x axis 
            xLabel = f"{30 - i*5} days ago"
            canvas.create_text(x, self.height - margin / 2, text=xLabel, font="Arial 12")

            # Draw dot
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
            points.append([x, y])
        
        # Draw point for today
        x = plotWidth + margin
        y = self.height - margin - int((self.today / yLabel) * plotHeight) + topMargin
        # Draw x label
        canvas.create_text(x, self.height - margin / 2, text="today", font="Arial 12")
        # Draw dot
        canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
        points.append([x, y])

        # Draw connecting lines 
        for j in range(len(points) - 1):
            canvas.create_line(points[j][0], points[j][1], points[j+1][0], 
                            points[j+1][1], fill="black", width=3)

    def redrawAll(self, canvas):
        try:
            self.drawIndividualFramework(self, canvas)
            self.drawIndividualPlot(self, canvas)
        except Exception as err:
            canvas.create_text(self.width / 2, self.height / 2, 
                              text=f"Rate limit exceeded. Try again later")


class MyModalApp(ModalApp):
    def appStarted(app):
        app.comparisonMode = ComparisonMode()
        app.currButton = None
        app.plotMode = PlotMode()
        app.setActiveMode(app.comparisonMode)
