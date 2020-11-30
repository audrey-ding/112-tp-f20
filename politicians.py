class Politician(object):
    def __init__(self, name, username, party):
        self.name = name
        self.party = party # "red" or "blue"
        self.username = username # Twitter username
        # self.pfp = None
        self.count = None

    def setCount(self, count):
        self.count = count