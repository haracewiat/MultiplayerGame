class Player:

    global playerVelocity
    global playerScore

    def __init__(self, x, y, colour, id):
        self.id = id
        self.x = x
        self.y = y
        self.playerVelocity = 9
        self.playerScore = 0
        self.colour = colour

    def increaseVelocity(self, newvelocity):
        playerVelocity += newvelocity
        return playerVelocity

    def increasePlayerScore(self, newScore):
        playerScore += newScore
        return playerScore

    def getVelocity(self):
        return playerVelocity