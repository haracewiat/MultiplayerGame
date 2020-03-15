class Player:

    def __init__(self, x, y, color, name):
        self.name = name
        self.x = x
        self.y = y
        self.playerVelocity = 9
        self.playerScore = 0
        self.color = color

    def increaseVelocity(self, newvelocity):
        self.playerVelocity += newvelocity
        return self.playerVelocity

    def increasePlayerScore(self, newScore):
        self.playerScore += newScore
        return self.playerScore

    def getVelocity(self):
        return self.playerVelocity