from player import *
from typing import List
# from food import *


class GameStateDTO:

    PLAYERS = List[Player]

    def __init__(self):
        self.PLAYERS = [Player(50, 50), Player(150, 150)]

    def update(self, state):
        self.PLAYERS = state

    def addPlayer(self, player: Player):
        # self.PLAYERS.append(player)
        self.PLAYERS = [player]

    def getPlayers(self):
        return self.PLAYERS

    def test(self):
        print(self)
