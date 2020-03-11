from player import *
from typing import List
# from food import *


class GameStateDTO:

    PLAYERS = List[Player]

    def __init__(self):
        print("Created a new game state.")

    def update(self, players: List[Player]):
        self.PLAYERS = players

    def getPlayers(self):
        return self.PLAYERS
