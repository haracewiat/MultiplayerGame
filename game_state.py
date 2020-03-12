from player import *
from typing import List
# from food import *


class GameStateDTO:

    PLAYERS = List[Player]

    def update(self, state):
        self.PLAYERS = state

    def addPlayer(self, player: Player):
        # self.PLAYERS.append(player)
        self.PLAYERS = [player]

    def updatePlayer(self, player, x, y):
        print(self.PLAYERS)

    def getPlayers(self):
        return self.PLAYERS

    def test(self):
        if self.PLAYERS is not None:
            print(self.PLAYERS)
        #print("X: " + self.PLAYERS[2].x + ", Y: " + self.PLAYERS[2].y)
