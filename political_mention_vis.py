# Audrey Ding @alding

# Using cmu_112_graphics from 15-112 course notes
# This file reads from the JSON file of tweet data and handles visualizations

from cmu_112_graphics import *
from tweet_scraping import *
from politicians import *
from datetime import date, timedelta
import math
import random

class StartMode(Mode):
    def appStarted(self):
        self.message = "Press s to start"

    # Referenced: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#ioMethods
    def keyPressed(self, event):
        if event.key == "s":
            strDate = self.getUserInput("Enter a date from the past year (YYYY-M-D):")
            if (strDate == None):
                self.message = "You cancelled, press s to try again"
            # Convert string date to datetime 
            try:
                # Referenced:
                # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
                # https://stackoverflow.com/questions/19480028/attributeerror-datetime-module-has-no-attribute-strptime
                self.app.date = datetime.datetime.strptime(strDate, "%Y-%m-%d")
            except ValueError as err:
                self.message = "Wrong date formatting, press s to try again"

            self.app.keyword = self.getUserInput("Enter a search keyword:")
            if (self.app.keyword == None):
                self.message = "You cancelled, press s to try again"

            if self.app.date != None and self.app.keyword != None:
                self.message = "Press enter to continue"

        if event.key == "Enter":
            self.app.setActiveMode(self.app.comparisonMode)

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/2, text="Political Tweet Analyzer",
                           font="Arial 18 bold")
        canvas.create_text(self.width/2, self.height/2 + 50, text=self.message,
                           font="Arial 14")

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

        self.getCounts()
        self.maxCount = self.greatestCount()
        
        self.buttons = []
        self.makeButtons()

    def getCounts(self):
        for politician in self.politicians:
            count = self.app.countUserKeywordTweets(politician.username, 
                                                    self.app.keyword, 
                                                    self.app.date)
            politician.setCount(count)

    def greatestCount(self):
        maxCount = 0
        for politician in self.politicians:
            if politician.count > maxCount:
                maxCount = politician.count
        return maxCount

    def mousePressed(self, event):
        for button in self.buttons:
            if self.pointInCircle(event.x, event.y, button.x, button.y, button.r):
                self.app.currPol = button.politician
                self.app.setActiveMode(self.app.plotMode)

    def pointInCircle(self, x0, y0, x1, y1, r):
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
        self.plotValues = []
        self.today = 0
        self.calculatePlotCounts()

    # Calculates 5-day-increment tweet frequencies (y-values to be plotted)
    # Returns list of y-values to be plotted and today's frequency
    #   Return today's frequency here to minimize how many times we scrape
    def calculatePlotCounts(self):
        # Datetime implementation from
        # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-5.php
        thirtyDaysAgo = date.today() - timedelta(21) # "since" arg is exclusive
        cumulative = []
        # Get cumulative counts for since 30 days ago, 25, 20, 15, ...
        for i in range(0, 21, 5):
            # Get since date and find cumulative count
            # Takes datetime.date, turns into string
            strDate = str(thirtyDaysAgo + timedelta(i)) 
            # Turns string into datetime.datetime
            dt = datetime.datetime.strptime(strDate, "%Y-%m-%d")
            count = self.app.countUserKeywordTweets(self.app.currPol.username, 
                                                        self.app.keyword, dt)
            print(f"{20 - i} days ago, {count}")
            cumulative.append(count)
        
        self.today = cumulative[len(cumulative) - 1]

        for j in range(len(cumulative) - 1):
            self.plotValues.append(cumulative[j] - cumulative[j + 1])

    def keyPressed(self, event):
        if event.key == "Enter":
            self.app.setActiveMode(self.app.similarityMode)

    def drawIndividualFramework(self, canvas):
        # Cover canvas
        canvas.create_rectangle(0, 0, self.width, self.height, fill="white")
        # Draw title 
        title = f"{self.app.currPol.name}'s tweets on \"{self.app.keyword}\""
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
            xLabel = f"{20 - i*5} days ago"
            canvas.create_text(x, self.height - margin / 2, text=xLabel, font="Arial 12")

            # Draw dot
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
            points.append([x, y])
        
        # Draw point for today
        x = plotWidth + margin
        y = self.height - margin - int((self.today / yLabel) * plotHeight)
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
            self.drawIndividualFramework(canvas)
            self.drawIndividualPlot(canvas)
            canvas.create_text(self.width/2, self.height - 10, 
                              text="Press enter to continue")
        except Exception as err:
            canvas.create_text(self.width / 2, self.height / 2, 
                              text=f"Error : {err}")

class SimilarityMode(Mode):
    def appStarted(self):
        # List that matches current user and keyword, from a date
        self.tweets = self.getUserKeywordTweets(self.app.currPol.username, 
                                                self.app.keyword, 
                                                self.app.date)
        self.similarTweet = ""
        self.similarTweetKeyword()

    # Returns tweets (text only) that match a user and keyword, from a date
    def getUserKeywordTweets(self, user, keyword, since):
        tweets = self.app.getTweetsFromDate(user, since)
        result = []
        for tweet in tweets:
            text = tweet[1]
            # Search isn't case sensitive
            if keyword.lower() in text.lower():
                result.append(text)
        return result

    def similarTweetKeyword(self):
        # Get random tweet from self.tweets
        randTweet = self.getRandomTweet(self.tweets)
        tweetWords = randTweet.split()
        maxWord = ""
        maxCounts = 0
        for word in tweetWords:
            if self.potentialKeyword(word):
                currCount = self.countKeyword(self.app.currPol.username, word)
                # Get potential keyword that was mentioned the most
                if currCount > maxCounts:
                    maxWord = word
                    maxCounts = currCount
        
        newKeywordTweets = self.getUserKeywordTweets(self.app.currPol.username, 
                                                     maxWord,
                                                     self.app.date)
        self.similarTweet = self.getRandomTweet(newKeywordTweets)

    def getRandomTweet(self, database):
        randInd = random.randint(0, len(database) - 1)
        return database[randInd]

    def potentialKeyword(self, word):
        # Articles, prepositions, and other filler words are usually short
        if len(word) < 4:
            return False
        # Potential keyword can't be current keyword that created self.tweets
        if word == self.app.keyword:
            return False
        # If is title case, then it's a proper noun, so potential keyword
        elif word[:1].isupper() and word[1:].islower():
            return True

    # Searches self.tweets for keyword and returns frequency
    def countKeyword(self, user, keyword):
        count = 0
        for tweet in self.tweets:
            text = tweet[1]
            # Search isn't case sensitive
            if keyword.lower() in text.lower():
                count += 1
        return count

    def drawSimilarTweet(self, canvas):
        canvas.create_text(self.width/2, self.height/2, text=self.similarTweet)

    def redrawAll(self, canvas):
        self.drawSimilarTweet(canvas)


class MyModalApp(ModalApp):
    def appStarted(app):
        app.tweetData = open("tweet_data.json").read()
        app.tweetDataJson = json.loads(app.tweetData)
        app.updateJson()

        app.date = None
        app.keyword = None
        app.startMode = StartMode()
        app.comparisonMode = ComparisonMode()
        app.currPol = None
        app.plotMode = PlotMode()
        app.similarityMode = SimilarityMode()
        app.setActiveMode(app.startMode)

    # Updates JSON file, if necessary, to include newest tweets
    def updateJson(app):    
        strLastUpdated = app.tweetDataJson["scrapeDate"] 
        lastUpdated = datetime.datetime.strptime(strLastUpdated, "%Y-%m-%d")
        strToday = str(date.today())
        today = datetime.datetime.strptime(strToday, "%Y-%m-%d")
        
        # Only update if last updated date wasn't today
        if lastUpdated != today:
            updatedData = {}
            updatedData["scrapeDate"] = str(date.today())
            for key in app.tweetDataJson:
                if key != "scrapeDate":
                    # Scrape from last updated date
                    newTweets = getTweets("user", key, lastUpdated)
                    oldTweets = app.tweetDataJson[user] # old tweets from the file
                    total = newTweets + oldTweets # combine new and old
                    updatedData[key] = total
            with open("tweet_data.json", "w") as outfile:
                json.dump(updatedData, outfile)
        else:
            print("Nothing to update")

    # Returns list of tweets from a specified date
    def getTweetsFromDate(app, user, targetDate):
        userTweets = app.tweetDataJson[user]
        i = 0
        while True:
            tweet = userTweets[i]
            strDate = tweet[0]
            # Convert string date to date
            currentDate = datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
            # Break out of loop if currentDate is earlier than targetDate
            # userTweets has most current tweets first
            if currentDate < targetDate: 
                break
            else:
                i += 1
    
        return userTweets[:i]

    # Returns count of tweets that match a user and keyword, from a specified date
    def countUserKeywordTweets(app, user, keyword, since):
        tweets = app.getTweetsFromDate(user, since)
        count = 0
        for tweet in tweets:
            text = tweet[1]
            # Search isn't case sensitive
            if keyword.lower() in text.lower():
                count += 1
        return count
