from player import *
from typing import List
# from food import *


class GameStateDTO:

    PLAYERS = []

    def update(self, state):
        self = state

    def addPlayer(self, player: Player):
        self.PLAYERS.append(player)

    def updatePlayer(self, player, x, y):
        self.PLAYERS.remove(player)
        self.addPlayer(Player(x, y))

    def getPlayers(self):
        return self.PLAYERS

    def test(self):
        for player in self.PLAYERS:
            print("X: " + str(player.x) + ", Y: " + str(player.y))
