class GameStateDTO:

    def __init__(self):
        self.players = []
        self.foods = []
        self.sentID = 0
        self.sequenceNumber = 0
        self.gameTime = ""

    def setPlayersList(self, players):
        self.players = players

    def setFoodsList(self, foods):
        self.foods = foods

    def setSentID(self, sentID):
        self.sentID = sentID

    def setSequenceNumber(self, sequenceNumber):
        self.sequenceNumber = sequenceNumber

    def setGameTime(self, gameTime):
        self.gameTime = gameTime

    def getPlayersList(self):
        return self.players

    def getFoodsList(self):
        return self.foods

    def getSentID(self):
        return self.sentID

    def getSequenceNumber(self):
        return self.sequenceNumber

    def getGameTime(self):
        return self.gameTime

    def setAllParameters(self, players, foods, sentID, sequenceNumber, gameTime):
        self.players = players
        self.foods = foods
        self.sentID = sentID
        self.sequenceNumber = sequenceNumber
        self.gameTime = gameTime