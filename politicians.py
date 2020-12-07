# This file contains the Politician, Button, and Point classes

class Politician(object):
    # A Politician has a name, Twitter username, and party
    def __init__(self, name, username, party):
        self.name = name
        self.party = party # "red" or "blue"
        self.username = username # Twitter username
        # self.pfp = None
        self.count = 0

    def setCount(self, count):
        self.count = count

class Button(object):
    # A Button has a center, radius, and Politician object 
    def __init__(self, x, y, r, politician):
        self.x = x
        self.y = y
        self.r = r
        self.politician = politician

class Point(object):
    # A Point has a center, radius, and list of tweets that match the query
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

