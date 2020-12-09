# Audrey Ding @alding

# Using cmu_112_graphics from 15-112 course notes
# This file reads from the JSON file of tweet data and handles visualizations

from cmu_112_graphics import * # import graphics
from tweet_scraping import * # (my file) import scraping functions
from politicians import * # (my file) import Politician, Button, Point, TweetBox
# From Python library:
from datetime import date, timedelta # https://docs.python.org/3/library/datetime.html
import math # https://docs.python.org/3/library/math.html
import random # https://docs.python.org/3/library/random.html 
import decimal

class StartMode(Mode):
    def appStarted(self):
        self.app.date = None
        self.app.keyword = None
        self.message = ""
        # Splash screen made on Canva, logo from
        # https://www.vhv.rs/viewpic/hTxToRJ_transparent-background-twitter-logo-hd-png-download/
        # Image implementation from:
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#loadImageUsingFile 
        self.screen = self.loadImage("start-screen.png")
            
    # Referenced: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#ioMethods
    def mousePressed(self, event):
        start = str(date.today() - timedelta(100))
        datePrompt = f"Enter a date from the past 100 days (after {start}) (YYYY-M-D):"
        strDate = self.getUserInput(datePrompt)
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
            self.app.setActiveMode(ChooseMode())
        
    
    # From 112 notes: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
    def rgbString(self, r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    def redrawAll(self, canvas):
        # Image implentation from
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#loadImageUsingFile
        canvas.create_image(self.width/2, self.height/2,
                            image=ImageTk.PhotoImage(self.screen))
        canvas.create_text(self.width/2, self.height - 25, text=self.message, 
                           fill="white", font="Helvetica 16")

class ChooseMode(Mode):
    def appStarted(self):
        self.app.makeNext()
        self.app.makeBack()

        self.app.politicians = [] # reset
        self.choices = [] # List of Choice objects
        self.makeChoices()

    def makeChoices(self):
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

        # Choice box width and height
        width = 300
        height = 50
        margin = 20 # margin between choice boxes
        # Height of entire matrix (all boxes together with margin)
        totalH = len(republicanUsers) * height + len(republicanUsers) * (margin-1)
        totalMargin = (self.height - totalH) / 2

        for i in range(len(republicanUsers)):
            republican = republicanUsers[i]
            x1 = self.width/2 - margin/2
            x0 = x1 - width
            y0 = totalMargin + (height + margin) * i
            y1 = y0 + height

            self.choices.append(Choice(republican[0], republican[1], "red", 
                                       x0, y0, x1, y1))

        for j in range(len(democraticUsers)):
            democrat = democraticUsers[j]
            x0 = self.width/2 + margin/2
            x1 = x0 + width
            y0 = totalMargin + (height + margin) * j
            y1 = y0 + height
            self.choices.append(Choice(democrat[0], democrat[1], "blue", 
                                       x0, y0, x1, y1))

    def mousePressed(self, event):
        # Loop through self.choices to see if they were clicked
        for choice in self.choices:
            if (event.x >= choice.x0 and event.x <= choice.x1 and
                event.y >= choice.y0 and event.y <= choice.y1):
                choice.clicked()
        # If next arrow clicked, go to Comparison Mode
        if (event.x >= self.app.next.x0 and event.x <= self.app.next.x1 and
            event.y >= self.app.next.y0 and event.y <= self.app.next.y1):
            self.setPoliticians()
            # Only go to Comparison Mode if politicians have been chosen
            if self.app.politicians != []:
                self.app.setActiveMode(ComparisonMode())
        # If back arrow clicked, go back to Start Mode
        elif (event.x >= self.app.back.x0 and event.x <= self.app.back.x1 and
              event.y >= self.app.back.y0 and event.y <= self.app.back.y1):
            self.app.setActiveMode(StartMode())
            
    def setPoliticians(self):
        # Loop through self.choices to find chosen ones
        for choice in self.choices:
            # If chosen, create Politician and add to app.politicians
            if choice.chosen:
                self.app.politicians.append(Politician(choice.name, 
                                                       choice.username, 
                                                       choice.party))

    # Loop through self.choices and draw them
    def drawChoices(self, canvas):
        for choice in self.choices:
            if choice.chosen: color = "grey"
            else: color = "white"
            canvas.create_rectangle(choice.x0, choice.y0, choice.x1, choice.y1,fill=color)
            x = (choice.x0 + choice.x1) / 2
            y = (choice.y0 + choice.y1) / 2
            canvas.create_text(x, y, text=choice.name, font="Helvetica 14")

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.choices[0].y0 - 50,
                           text="Click to choose politicians to compare",
                           font="Helvetica 16 bold")
        self.app.drawNext(canvas)
        self.app.drawBack(canvas)
        self.drawChoices(canvas)
    
class ComparisonMode(Mode):
    def appStarted(self):
        self.app.makeBack()
        
        self.app.curPol = None

        self.getCounts()
        self.maxCount = self.greatestCount()
        
        self.rows = 0
        self.cols = 0
        self.getRowsCols()
        self.margin = 20 # margin around sides and bottom
        self.topMargin = 70 
        # Next two lines from 112 getCellBounds()
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
        self.cellWidth  = (self.width - 2*self.margin) / self.cols
        self.cellHeight = (self.height - self.margin - self.topMargin) / self.rows

        self.buttons = []
        self.makeButtons()
    
    def mousePressed(self, event):
        for button in self.buttons:
            if self.app.pointInCircle(event.x, event.y, button.x, button.y, 
                                        button.r):
                self.app.currPol = button.politician
                self.app.setActiveMode(PlotMode())

        # If back arrow clicked, go back to Choose Mode
        if (event.x >= self.app.back.x0 and event.x <= self.app.back.x1 and
              event.y >= self.app.back.y0 and event.y <= self.app.back.y1):
            self.app.setActiveMode(ChooseMode())
        

    def getCounts(self):
        for politician in self.app.politicians:
            tweets = self.app.getTweetsFromDate(politician.username, self.app.date)
            count = self.app.countKeywordTweets(self.app.keyword, tweets)
            politician.setCount(count)

    def greatestCount(self):
        maxCount = 0
        for politician in self.app.politicians:
            if politician.count > maxCount:
                maxCount = politician.count
        return maxCount

    # Calculates how many rows, columns for optimal button placement
    def getRowsCols(self):
        total = len(self.app.politicians)
        sqrt = total**0.5
        # is_integer(): https://docs.python.org/3/library/stdtypes.html#float.is_integer
        # If total is perfect square, then we're done
        if sqrt.is_integer():
            self.rows = int(sqrt)
            self.cols = int(sqrt)
        else:
            factor = self.roundHalfUp(sqrt) # round sqrt
            i = 0
            # Find dimensions whose product is closest to total
            while factor * i < total:
                i += 1
            # Canvas is rectangular, so rows should be < cols
            self.rows = int(min(factor, i))
            self.cols = int(max(factor, i))

    # From 112 notes: 
    # https://www.cs.cmu.edu/~112/notes/notes-variables-and-functions.html#RecommendedFunctions
    def roundHalfUp(self, d):
        import decimal
        rounding = decimal.ROUND_HALF_UP
        return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

    def makeButtons(self):
        polIndex = 0
        for row in range(self.rows):
            for col in range(self.cols):
                currentPol = self.app.politicians[polIndex]
                maxR = min(self.cellWidth, self.cellHeight) / 2
                # No one mentioned, so no circle 
                if self.maxCount == 0:
                    r = 0
                # Otherwise,cxalculate radius based on proportion with maxCount
                else:
                    r = (currentPol.count / self.maxCount) * maxR
                (x0, y0, x1, y1) = self.getCellBounds(row, col)
                x = (x0 + x1) / 2
                y = (y0 + y1) / 2
                self.buttons.append(Button(x, y, r, currentPol))
                # Break out of loop if no more politicians to create buttons for
                if polIndex + 1 == len(self.app.politicians):
                    break
                else:
                    polIndex += 1

    # From 112 notes: 
    # https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids 
    # Returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    def getCellBounds(self, row, col):
        x0 = self.margin + col * self.cellWidth
        x1 = x0 + self.cellWidth
        y0 = self.topMargin + row * self.cellHeight
        y1 = y0 + self.cellHeight
        return (x0, y0, x1, y1)

    # Loop through buttons and draw them
    def drawButtons(self, canvas):
        for button in self.buttons:
            x = button.x
            y = button.y
            r = button.r
            # Draw buttons
            canvas.create_oval(x - r, y - r, x + r, y + r, fill=button.politician.party, width=0)
            # Draw politician name and count
            canvas.create_text(x, y, text=button.politician.count, font="Helvetica 12")
            canvas.create_text(x, y + 30, text=button.politician.name, font="Helvetica 12")

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, 20, 
                           text=f"Frequencies of {self.app.keyword} since {self.app.date}",
                           font="Helvetica 16 bold")
        self.drawButtons(canvas)
        self.app.drawBack(canvas)
        

class PlotMode(Mode):
    def appStarted(self):
        self.app.makeBack()

        self.points = [] # list of Points
        self.counts = [] # list of counts for 5-day increments
        self.calculateCounts()

        self.xMargin = 50 # margins for graph framework
        self.yMargin = 100
        self.yLabel = 0 # label on y axis 
        self.makePoints()

    # Calculates 5-day-increment tweet frequencies (y-values to be plotted)
    # Returns list of y-values to be plotted and today's frequency
    #   Return today's frequency here to minimize how many times we scrape
    def calculateCounts(self):
        # Datetime implementation from
        # https://www.w3resource.com/python-exercises/date-time-exercise/python-date-time-exercise-5.php
        thirtyDaysAgo = date.today() - timedelta(31) # "since" arg is exclusive
        cumulative = []
        # Get cumulative counts for since 30 days ago, 25, 20, 15, ...
        for i in range(0, 31, 5):
            # Get since date and find cumulative count
            start = self.app.dateToDatetime(thirtyDaysAgo) + timedelta(i)
            # If it's the last point, it's today, so can't add 5
            if i == 30:
                end = start + timedelta(1) # today
            else:
                end = start + timedelta(5)
            # Tweet list that matches date range and user
            generalTweets = self.app.getTweetsDateRange(self.app.currPol.username, 
                                                        start, end)
            # Tweet list that matches keyword too
            tweets = self.app.getKeywordTweets(self.app.keyword, generalTweets)
            # Create Point with list of tweets, append to self.points
            self.points.append(Point(tweets))
            # Count of tweets that match keyword, append to self.counts
            count = self.app.countKeywordTweets(self.app.keyword, tweets) 
            self.counts.append(count)

    def makePoints(self):
        plotWidth = self.width - self.xMargin * 2
        plotHeight = self.height - self.yMargin * 2

        # Largest count that determines y axis scale
        maxCount = max(self.counts) 
        # No mentions in the past 30 days
        if maxCount == 0:
            self.yLabel = 1 # don't want to divide by 0
        else:
            # Otherwise, round to nearest ten for label
            self.yLabel = int(math.ceil(maxCount / 10) * 10)

        for i in range(len(self.counts)):
            x = int(plotWidth / (len(self.counts) - 1)) * i + self.xMargin
            y = (self.height - self.yMargin - 
                int((self.counts[i] / self.yLabel) * plotHeight))
            # If it's the last point, it is today
            if i == len(self.counts) - 1:
                xLabel = "today"
            else:
                xLabel = f"{30 - i*5} days ago"
            currPoint = self.points[i]
            currPoint.setAttributes(x, y, 5, xLabel)

    def mousePressed(self, event):
        for point in self.points:
            if self.app.pointInCircle(event.x, event.y, point.x, point.y, point.r):
                # No tweets to show
                if point.tweets == []:
                    self.app.setActiveMode(NoPointMode())
                else:
                    self.app.currPoint = point
                    self.app.setActiveMode(PointMode())
        
        # If back arrow clicked, go back to Comparison Mode
        if (event.x >= self.app.back.x0 and event.x <= self.app.back.x1 and
              event.y >= self.app.back.y0 and event.y <= self.app.back.y1):
            self.app.setActiveMode(ComparisonMode())

    def drawFramework(self, canvas):
        # Cover canvas
        canvas.create_rectangle(0, 0, self.width, self.height, fill="white")
        # Draw title 
        title = f"{self.app.currPol.name}'s tweets on \"{self.app.keyword}\""
        canvas.create_text(self.width / 2, 50, text=title, font="Helvetica 18 bold")
        # Clicky point instruction
        point = "Click on a point for a tweet"
        canvas.create_text(self.width / 2, 75, text=point, font="Helvetica 14")
        # Draw plot frame with margins
        canvas.create_rectangle(self.xMargin, self.yMargin, 
                                self.width - self.xMargin, 
                                self.height - self.yMargin) 

    def drawPlot(self, canvas):
        # Draw yLabel on y axis
        canvas.create_text(self.xMargin - 10, self.yMargin, text=self.yLabel, 
                           font="Helvetica 12")

        # Loop through Points, draw dots, draw x labels, and draw lines
        for i in range(len(self.points)):
            x = self.points[i].x
            y = self.points[i].y
            xLabel = self.points[i].xLabel
            # Draw dot
            canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")
            # Draw x label
            canvas.create_text(x, self.height - self.yMargin + 15, text=xLabel, 
                            font="Helvetica 12")
            # Draw connecting line to next point, but only if not at last point
            if i != len(self.points) - 1:
                x1 = self.points[i + 1].x
                y1 = self.points[i + 1].y
                canvas.create_line(x, y, x1, y1, fill="black", width = 3)

    def redrawAll(self, canvas):
        self.drawFramework(canvas)
        self.drawPlot(canvas)
        self.app.drawBack(canvas)

class NoPointMode(Mode):
    def appStarted(self):
        self.app.makeBack()

    def mousePressed(self, event):
        # If back arrow clicked, go back to Comparison Mode
        if (event.x >= self.app.back.x0 and event.x <= self.app.back.x1 and
              event.y >= self.app.back.y0 and event.y <= self.app.back.y1):
            self.app.setActiveMode(ComparisonMode())

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height/2, text="No tweets to show",
                           font="Helvetica 16")
        self.app.drawBack(canvas)

    
class PointMode(Mode):
    def appStarted(self):
        self.app.makeBack()
        self.up = None
        self.down = None
        self.makeUpDown()

        self.shift = 0
        self.tweets = self.app.currPoint.tweets # simpler variable to look at
        self.tweetBoxes = [] # list of TweetBoxes
        self.makeTweetBoxes()
        self.positionTweetBoxes()

    # Make up and down Arrows
    def makeUpDown(self):
        # Image from https://thenounproject.com/term/up-button/1384177/ 
        # Same images, just flipped
        down = self.loadImage("down-arrow.png")
        up = self.loadImage("up-arrow.png")
        margin = 15
        width, height = down.size # images have same size

        downX1 = self.width - margin
        downX0 = downX1 - width
        downY1 = self.height - margin
        downY0 = downY1 - height
        self.down = Arrow(downX0, downY0, downX1, downY1, down)

        upX1 = downX1
        upX0 = downX0
        upY1 = downY0 
        upY0 = upY1 - height
        self.up = Arrow(upX0, upY0, upX1, upY1, up)


    def timerFired(self):
        self.positionTweetBoxes()
        
    def mousePressed(self, event):
        # Loop through tweet boxes to check if clicked
        for tweetBox in self.tweetBoxes:
            if (event.x >= tweetBox.x0 and event.x <= tweetBox.x1 and
                event.y >= tweetBox.y0 and event.y <= tweetBox.y1):
                self.app.currTweetBox = tweetBox 
                self.app.setActiveMode(SimilarityMode())

        # If back arrow clicked, go back to Plot Mode
        if (event.x >= self.app.back.x0 and event.x <= self.app.back.x1 and
              event.y >= self.app.back.y0 and event.y <= self.app.back.y1):
            self.app.setActiveMode(PlotMode())

        # If down arrow clicked, scroll down
        if (event.x >= self.down.x0 and event.x <= self.down.x1 and
            event.y >= self.down.y0 and event.y <= self.down.y1):
            # Only scroll down if there are more boxes below
            if self.shift + 1 <= len(self.tweetBoxes):
                self.shift += 1

        # If up arrow clicked, scroll up
        if (event.x >= self.up.x0 and event.x <= self.up.x1 and
            event.y >= self.up.y0 and event.y <= self.up.y1):
            # Only scroll up if there are more boxes above
            if self.shift -1 >= 0:
                self.shift -= 1        
        
    # Create TweetBox objects with display, header, and coords=0
    def makeTweetBoxes(self):
        for tweet in self.tweets:
            display = self.app.formatTweet(tweet[1]) # formatted tweet
            strDate = tweet[0]
            dateWithTime = datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
            date = dateWithTime.date() # published date (date obj)
            header = f"{self.app.currPol.name} @{self.app.currPol.username} • {date}"

            self.tweetBoxes.append(TweetBox(0, 0, 0, 0, tweet, display, header))

    def positionTweetBoxes(self):
        for i in range(self.shift, len(self.tweetBoxes)):
            tweetBox = self.tweetBoxes[i]

            boxWidth = self.app.maxCharCount(tweetBox.display, tweetBox.header) * 7.5 + 20 # margins

            boxHeight = (len(tweetBox.display) + 1) * 20 + 15 # lines and header

            x0 = self.width/2 - boxWidth/2
            x1 = self.width/2 + boxWidth/2
            # First tweet box, leave a margin of 50px
            if i == self.shift:
                y0 = 50
            # Other tweet box y position depends on previous tweet box
            else: 
                y0 = self.tweetBoxes[i - 1].y1 + 20 # 20px margin 
            y1 = y0 + boxHeight
            
            tweetBox.position(x0, y0, x1, y1)
            self.consistentBoxWidth()

    # Find max box width and set it as all tweet boxes' width (for consistency)
    def consistentBoxWidth(self):
        maxWidth = 0
        # Get max width
        for tweetBox in self.tweetBoxes:
            if tweetBox.x1 - tweetBox.x0 > maxWidth:
                maxWidth = tweetBox.x1 - tweetBox.x0
        # Set max width for every tweet box
        for tweetBox in self.tweetBoxes:
            x0 = self.width/2 - maxWidth/2
            x1 = self.width/2 + maxWidth/2
            tweetBox.setWidth(x0, x1)    

    # Loop through self.tweetBoxes and draw them
    def drawTweetBoxes(self, canvas):
        for i in range(self.shift, len(self.tweetBoxes)):
            tweetBox = self.tweetBoxes[i]
            # Don't want to draw out of bounds
            if tweetBox.y1 > self.height:
                break
            canvas.create_rectangle(tweetBox.x0, tweetBox.y0, tweetBox.x1, 
                                    tweetBox.y1)
            canvas.create_text(tweetBox.x0 + 10, tweetBox.y0 + 15, 
                               text=tweetBox.header, anchor=W, 
                               font="Helvetica 16 bold")
            for i in range(len(tweetBox.display)):
                canvas.create_text(tweetBox.x0 + 10, tweetBox.y0 + 35 + i*20, 
                                   text=tweetBox.display[i].encode("unicode-escape"), anchor=W, 
                                   font="Helvetica 16")

    def drawUpDown(self, canvas):
        upX = (self.up.x0 + self.up.x1) / 2
        upY = (self.up.y0 + self.up.y1) / 2
        canvas.create_image(upX, upY, image=ImageTk.PhotoImage(self.up.image))

        downX = (self.down.x0 + self.down.x1) / 2
        downY = (self.down.y0 + self.down.y1) / 2
        canvas.create_image(downX, downY, image=ImageTk.PhotoImage(self.down.image))

    def redrawAll(self, canvas):
        canvas.create_text(self.width/2, self.height + 20, 
                           text="Click on a tweet to see a similar tweet",
                           font="Helvetica 16")
        self.drawTweetBoxes(canvas)
        self.app.drawBack(canvas)
        self.drawUpDown(canvas)

class SimilarityMode(Mode):
    def appStarted(self):
        self.app.makeBack()

        self.tweets = self.app.tweetDataJson[self.app.currPol.username]
        self.similarTweet = None
        
        self.similarFromEntity("hashtag")
        self.similarFromEntity("mention")
        self.similarFromWord()

        self.tweetBoxes = []
        self.makeCurrTweetBox()
        self.makeSimilarTweetBox()

    def mousePressed(self, event):
        # If back arrow clicked, go back to Point Mode
        if (event.x >= self.app.back.x0 and event.x <= self.app.back.x1 and
              event.y >= self.app.back.y0 and event.y <= self.app.back.y1):
            self.app.setActiveMode(PointMode())
        
    # Find tweets that match app.currTweetBox's entities
    def similarFromEntity(self, hashtagOrMention):
        if hashtagOrMention == "hashtag":
            x = 2 # hashtag is 3rd element of a tweet
        else:
            x = 3 # mention is 4th element of a tweet
        entities = self.app.currTweetBox.tweet[x] # list of mentioned usernames
        if entities != []:
            self.tweets = self.searchForEntities(x, entities, self.tweets)

    # Takes list of tweets, returns subset of tweets that matches entities
    def searchForEntities(self, index, entities, tweets):
        result = []
        # Loop through tweets
        for tweet in tweets:
            # Loop through entities
            for entity in entities:
                # If the entity is in tweet's list of entities 
                #   and the tweet is not already in result, add to result
                if entity in tweet[index] and tweet not in result:
                    result.append(tweet)
        return result

    def similarFromWord(self):
        tweetWords = self.app.currTweetBox.tweet[1].split()
        maxWord = ""
        maxCounts = 0
        for word in tweetWords:
            if self.potentialKeyword(word):
                currCount = self.app.countKeywordTweets(word, self.tweets)
                # Get potential keyword that was mentioned the most
                if currCount > maxCounts:
                    maxWord = word
                    maxCounts = currCount
        
        newKeywordTweets = self.app.getKeywordTweets(maxWord, self.tweets)
        if self.app.currTweetBox.tweet != self.similarTweet:
            self.similarTweet = self.app.getRandomElement(newKeywordTweets)

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

    def makeCurrTweetBox(self):
        # Account for margins
        boxWidth = (self.app.maxCharCount(self.app.currTweetBox.display, 
                    self.app.currTweetBox.header) * 7 + 20)
        boxHeight = (len(self.app.currTweetBox.display) + 1) * 20 + 15 

        x0 = self.width/2 - boxWidth/2
        y0 = self.height/2 - boxHeight - 35 # 70 px margin between two boxes
        x1 = self.width/2 + boxWidth/2
        y1 = y0 + boxHeight

        # Update position and append to list of TweetBoxes to draw later
        self.app.currTweetBox.position(x0, y0, x1, y1)
        self.tweetBoxes.append(self.app.currTweetBox)

    def makeSimilarTweetBox(self):
        display = self.app.formatTweet(self.similarTweet[1])

        strDate = self.similarTweet[0]
        dateWithTime = datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
        date = dateWithTime.date()
        header = f"{self.app.currPol.name} @{self.app.currPol.username} • {date}"

        boxWidth = self.app.maxCharCount(display, header) * 7 + 20 # margins
        boxHeight = (len(display) + 1) * 20 + 15 # lines and header

        x0 = self.width/2 - boxWidth/2
        y0 = self.height/2 + 35 # 70 px margin between boxes
        x1 = self.width/2 + boxWidth/2
        y1 = y0 + boxHeight
        
        self.tweetBoxes.append(TweetBox(x0, y0, x1, y1, self.similarTweet, display, header))

    def drawTweetBoxes(self, canvas):
        # Loop through self.tweetBoxes and draw them
        for tweetBox in self.tweetBoxes:
            # Draw box
            canvas.create_rectangle(tweetBox.x0, tweetBox.y0, 
                                    tweetBox.x1, tweetBox.y1)
            # Draw header
            canvas.create_text(tweetBox.x0 + 10, tweetBox.y0 + 15, 
                               text=tweetBox.header, anchor=W,
                               font="Helvetica 16 bold")
            # Draw formatted tweet by looping through display
            for i in range(len(tweetBox.display)):
                canvas.create_text(tweetBox.x0 + 10, tweetBox.y0 + 35 + i*20, 
                                   text=tweetBox.display[i], anchor=W, 
                                   font="Helvetica 16")

    def redrawAll(self, canvas):
        self.drawTweetBoxes(canvas)
        # Header for curr tweet box
        canvas.create_text(self.width/2, self.app.currTweetBox.y0 - 25,
                           text="Clicked tweet", font="Helvetica 18 bold")
        # Header for similar tweet box (2nd elem in self.tweetBoxes)
        canvas.create_text(self.width/2, self.tweetBoxes[1].y0 - 25,
                           text="Similar tweet", font="Helvetica 18 bold")

        self.app.drawBack(canvas)

class MyModalApp(ModalApp):
    def appStarted(app):
        app.tweetData = open("tweet_data.json").read()
        app.tweetDataJson = json.loads(app.tweetData)
        # app.updateJson()
        app.next = None
        app.back = None

        app.politicians = []
        app.date = None
        app.keyword = None
        app.currPol = None
        app.currPoint = None
        app.currTweetBox = None

        app.setActiveMode(StartMode())

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

    # Make next Arrow
    def makeNext(app):
        # Image from https://www.pngitem.com/so/back-button/ (flipped)
        nextImage = app.loadImage("right-arrow.png")
        margin = 25

        # Image size implementation:
        # https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#imageSize
        nextWidth, nextHeight = nextImage.size
        nextX1 = app.width - margin
        nextX0 = nextX1 - nextWidth
        nextY1 = app.height - margin
        nextY0 = nextY1 - nextHeight
        app.next = Arrow(nextX0, nextY0, nextX1, nextY1, nextImage)

    # Make back Arrow
    def makeBack(app):
        # Image from https://www.pngitem.com/so/back-button/
        backImage = app.loadImage("left-arrow.png")
        margin = 25

        backWidth, backHeight = backImage.size
        backX0 = margin
        backX1 = backX0 + backWidth
        backY0 = margin
        backY1 = backY0 + backHeight
        app.back = Arrow(backX0, backY0, backX1, backY1, backImage)

    # Draw next arrow image
    def drawNext(app, canvas):
        nextX = (app.next.x0 + app.next.x1) / 2
        nextY = (app.next.y0 + app.next.y1) / 2
        canvas.create_image(nextX, nextY, image=ImageTk.PhotoImage(app.next.image))

    # Draw back arrow image
    def drawBack(app, canvas):
        backX = (app.back.x0 + app.back.x1) / 2
        backY = (app.back.y0 + app.back.y1) / 2
        canvas.create_image(backX, backY, image=ImageTk.PhotoImage(app.back.image))

    # Returns list of tweets from a specified datetime
    def getTweetsFromDate(app, user, targetDate):
        userTweets = app.tweetDataJson[user]
        i = 0
        # userTweets can't be empty
        while userTweets != [] and i < len(userTweets):
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

    def getTweetsDateRange(app, user, start, end):
        subset = app.getTweetsFromDate(user, start)
        i = 0
        # subset can't be empty
        while subset != [] and i < len(subset):
            tweet = subset[i]
            strDate = tweet[0]
            # Convert string date to date
            currentDate = datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")
            # Break out of loop if end is earlier than targetDate
            # subset has most current tweets first
            if currentDate < end:
                break
            else:
                i += 1
        return subset[i + 1:]

    # Returns tweets that match a keyword, from a list of tweets 
    def getKeywordTweets(app, keyword, tweets):
        result = []
        for tweet in tweets:
            text = tweet[1]
            search = keyword.lower() + " "
            # Search isn't case sensitive
            if search in text.lower():
                result.append(tweet)
        return result

    # Returns count of tweets that match a keyword, from a list of tweets
    def countKeywordTweets(app, keyword, tweets):
        count = 0
        for tweet in tweets:
            text = tweet[1]
            search = keyword.lower() + " "
            # Search isn't case sensitive
            if search in text.lower():
                count += 1
        return count

    def pointInCircle(app, x0, y0, x1, y1, r):
        return ((x1 - x0)**2 + (y1 - y0)**2)**0.5 <= r

    def dateToDatetime(app, date):
        strDate = str(date)
        return datetime.datetime.strptime(strDate, "%Y-%m-%d")

    def getRandomElement(app, database):
        randInd = random.randint(0, len(database) - 1)
        return database[randInd]

    def formatTweet(app, tweetText):
        display = []
        count = 0
        line = ""
        # Ignores emojis so there is no unicode error in displaying them
        # Next 2 lines: 
        # https://www.kite.com/python/answers/how-to-remove-non-ascii-characters-in-python
        encoded = tweetText.encode("ascii", "ignore")
        decoded = encoded.decode()
        for word in decoded.split():
            count += len(word) + 1 # space is a character too
            if count < 50:
                line += word + " "
            else:
                display.append(line) # add line to list of lines
                # Word goes in new line
                count = len(word) + 1 # reset count
                line = word + " " # add word to the next line
        display.append(line) # last line
        return display

    # Returns number of characters in longest line, incl header
    def maxCharCount(app, display, header):
        maxCount = len(header)
        maxLine = header
        for line in display:
            if len(line) > maxCount:
                maxCount = len(line)
                maxLine = line
        return maxCount
