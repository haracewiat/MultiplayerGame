class Player:

    def __init__(self, x, y, color, name, id):
        self.name = name
        self.x = x
        self.y = y
        self.playerVelocity = 18
        self.playerScore = 0
        self.color = color
        self.id = id

    def increaseVelocity(self, velocity):
        self.playerVelocity += velocity
        return self.playerVelocity

    def increasePlayerScore(self, score):
        self.playerScore += score
        return self.playerScore

    def decreasePlayerScoreAndIncreaseVelocity(self):
        self.playerScore = (int(self.playerScore-1))
        print(self.playerScore)
        self.playerVelocity = (int(self.playerVelocity+1))
        print(self.playerVelocity)

    def getVelocity(self):
        return self.playerVelocity

    def getScore(self):
        return self.playerScore

    def getId(self):
        return self.id
