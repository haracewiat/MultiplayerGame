import pygame
import threading
from player import Player
from client import Client
from game_state import *
from typing import List

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SIZE = (700, 500)


class Game:

    GAME_STATE = GameStateDTO()
    connection = Client()
    screen = pygame.display.set_mode(SIZE)
    clock = pygame.time.Clock()
    connected = True

    def __init__(self):

        # Watch the game state
        thread_receive = threading.Thread(target=self.watchGameState)
        thread_receive.start()

        # Spawn a new player
        player = self.spawnPlayer()

        while self.connected:

            self.clock.tick(60)

            # QUIT FIXME put in seperate funtion + add escape
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.connected = False

            self.screen.fill(WHITE)

            # FIXME case for an empty list
            # print(self.GAME_STATE.getPlayers())
            # for player in self.GAME_STATE.getPlayers():
            #    player.draw(self.screen)

            # Player movement
            player.draw(self.screen)
            self.movePlayer(pygame.key.get_pressed(), player)

            pygame.display.flip()

        # Close the window and quit.
        pygame.quit()

    def watchGameState(self):
        self.GAME_STATE.update(self.connection.receive())
        # print(self.GAME_STATE)

    def spawnPlayer(self):
        player = Player(450, 450)
        self.GAME_STATE.addPlayer(player)
        self.connection.send(self.GAME_STATE)
        return player

    def movePlayer(self, keys, player):

        if keys[pygame.K_RIGHT]:
            if player.x <= SIZE[0] - player.velocity:
                player.move(0)

        if keys[pygame.K_LEFT]:
            if player.x >= player.velocity:
                player.move(1)

        if keys[pygame.K_UP]:
            if player.y >= player.velocity:
                player.move(2)

        if keys[pygame.K_DOWN]:
            if player.y <= SIZE[1] - player.velocity:
                player.move(3)


game = Game()
