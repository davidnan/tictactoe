class Player:
    def __init__(self):
        self.name = None
        self.score = 0
        self.ch = None

    def incrementScore(self):
        self.score = self.score + 1

    def changeName(self, name):
        self.name = name

    def setCh(self, ch):
        self.ch = ch

    def getCh(self): return self.ch
    def getName(self): return self.name
    def getScore(self): return self.score

