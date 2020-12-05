# Audrey Ding @alding

from tweet_scraping import *
from cmu_112_graphics import *
from political_mention_vis import *

if (__name__ == '__main__'):
    try:
        MyModalApp(width=1000, height=800)
    except Exception as err:
        print(f"There was an error: {err}")