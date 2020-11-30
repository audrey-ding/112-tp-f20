# Audrey Ding @alding

from cmu_112_graphics import *
from tweet_scraping import *
import random


def appStarted(app):
    app.userOrSearch = "user" 
    app.user = "joebiden"
    app.since = "2020-11-22"
    app.tweets = getTweets(app.userOrSearch, app.user, app.since)
    app.count = len(app.tweets)

    randomIndex = random.randint(0, app.count - 1)
    app.randTweet = app.tweets[randomIndex]

def redrawAll(app, canvas):
    displayCount = f"@{app.user} has tweeted {app.count} times since {app.since}"
    canvas.create_text(400, 50, text=displayCount)
    title = f"Here's a random tweet from {app.user} from any time since {app.since}: "
    canvas.create_text(400, 150, text=title)
    canvas.create_text(400, 200, text=app.randTweet)

#HELLO

