class Politician(object):
    def __init__(self, name, username, party):
        self.name = name
        self.party = party # "red" or "blue"
        self.username = username # Twitter username
        # self.pfp = None
        self.count = 0

    def setCount(self, count):
        self.count = count

    def setButton(self, button):
        self.button = button

class Button(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r