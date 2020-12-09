# This file contains the Politician, Button, and Point classes

# A Choice has a name, Twitter username, party, boolean value chosen, 
#   and position coords
class Choice(object):
    def __init__(self, name, username, party, chosen, x0, y0, x1, y1):
        self.name = name
        self.party = party # "red" or "blue"
        self.username = username # Twitter username
        self.chosen = 0
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

# A Politician has a name, Twitter username, and party, and count of tweets
class Politician(object):
    def __init__(self, name, username, party):
        self.name = name
        self.party = party # "red" or "blue"
        self.username = username # Twitter username
        # self.pfp = None
        self.count = 0

    def setCount(self, count):
        self.count = count

# A Button has a center, radius, and Politician object 
class Button(object):
    def __init__(self, x, y, r, politician):
        self.x = x
        self.y = y
        self.r = r
        self.politician = politician

# A Point has a center, radius, and list of tweets that match the query
class Point(object):
    def __init__(self, tweets):
        self.tweets = tweets
        self.x = 0
        self.y = 0
        self.r = 0
        self.xLabel = 0

    def setAttributes(self, x, y, r, xLabel):
        self.x = x
        self.y = y
        self.r = r
        self.xLabel = xLabel

# A TweetBox has coords, tweet, display (foormatted tweet), and a header
class TweetBox(object):
    def __init__(self, x0, y0, x1, y1, tweet, display, header):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.tweet = tweet
        self.display = display
        self.header = header
    
    def position(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def setWidth(self, x0, x1):
        self.x0 = x0
        self.x1 = x1