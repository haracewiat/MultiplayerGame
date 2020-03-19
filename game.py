# small network game that has differnt blobs
# moving around the screen

import os
import random
from client import Client
# from client import queue
import threading

import contextlib
from constants import colors as COLORS
from gameStateDTO import *
import math


with contextlib.redirect_stdout(None):
    import pygame

pygame.font.init()

PLAYER_RADIUS = 18
START_VEL = 18
BALL_RADIUS = 10
ROUND_TIME = 600
WIDTH, HEIGHT = 1200, 700
MIN_VELOCITY = 4
FPS = 30

NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)


# Dynamic Variables
players = {}
foods = []


class Game:

    running = True
    velocity = 0

    def __init__(self):
        # get users name
        while True:
            name = input("Please enter your name: ")
            if 0 < len(name) < 20:
                break
            else:
                print(
                    "Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

        # setup pygame window
        self.WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

        # start game
        self.run(name)

    def run(self, name):
        global players

        # start by connecting to the network
        client = Client()
        current_id = client.connect(name)
        client.send(GameStateDTO('get', None, None, None, None))
        foods, players, game_time = client.receive()
        player = players[current_id]

        # setup the clock
        clock = pygame.time.Clock()

        # Watch the game state updates
        thread_receive = threading.Thread(target=client.watchGameState)
        thread_receive.start()

        while self.running:
            # Set frames per second
            clock.tick(FPS)

            # Adjust player's velocity
            self.setVelocity(player)

            # Move the player
            self.movePlayer(player, pygame.key.get_pressed(), self.velocity)

            # Sent the client's game state
            client.send(GameStateDTO('MOVE', player.x, player.y,
                                     player.playerScore, player.playerVelocity))

            # Update the game state to the most recent one
            if not client.queue.empty():
                foods, players, game_time = client.queue.get(0)

            # See if player ate food
            check_collision(player, foods)

            # Exit the game if applicable
            self.exit(client)

            # Refresh the window with new game state
            self.refresh(player, players, foods, game_time, player.playerScore)

            # Update the frame
            pygame.display.update()

        thread_receive.join()
        client.disconnect()
        pygame.quit()
        quit()

    def movePlayer(self, player, keys, velocity):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if player.x + velocity + PLAYER_RADIUS <= WIDTH:
                player.x = player.x + velocity

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if player.x - velocity - PLAYER_RADIUS >= 0:
                player.x = player.x - velocity

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if player.y - velocity - PLAYER_RADIUS >= 0:
                player.y = player.y - velocity

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if player.y + velocity + PLAYER_RADIUS <= HEIGHT:
                player.y = player.y + velocity

        if keys[pygame.K_SPACE]:
            player.decreasePlayerScoreAndIncreaseVelocity()
            # player.printEatenFoodsList()

    def exit(self, client):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                client.watching = False
                client.sock.shutdown(1)

    def setVelocity(self, player):
        velocity = (START_VEL - round(player.increasePlayerScore(0)))
        self.velocity = MIN_VELOCITY if velocity <= MIN_VELOCITY else velocity

    def convert_time(self, t):
        """
        converts a time given in seconds to a time in
        minutes

        :param t: int
        :return: string
        """
        t = ROUND_TIME - t
        time = str(t)
        return time

    def refresh(self, player, players, foods, game_time, score):
        """
        draws each frame
        :return: None
        """
        self.WINDOW.fill(
            (255, 255, 255))  # fill screen white, to clear old frames

        # draw me (client side prediction)
        pygame.draw.circle(self.WINDOW, player.color,
                           (player.x, player.y), PLAYER_RADIUS)
        text = NAME_FONT.render(player.name, 1, (0, 0, 0))
        self.WINDOW.blit(text, (player.x - text.get_width() /
                                2, player.y - text.get_height() / 2))

        # draw all the orbs/foods
        for food in foods:
            pygame.draw.circle(self.WINDOW, food.colour,
                               (food.x, food.y), BALL_RADIUS)

        # draw each player in the list except me
        for otherPlayer in sorted(players, key=lambda x: players[x].playerScore):
            # print(player.id)
            p = players[otherPlayer]
            print(p.id)
            if (player.id != p.id):
                pygame.draw.circle(self.WINDOW, p.color,
                                   (p.x, p.y), PLAYER_RADIUS)
                # render and draw name for each player
                text = NAME_FONT.render(p.name, 1, (0, 0, 0))
                self.WINDOW.blit(text, (p.x - text.get_width() /
                                        2, p.y - text.get_height() / 2))

        # draw scoreboard
        sort_players = list(
            reversed(sorted(players, key=lambda x: players[x].playerScore)))
        title = TIME_FONT.render("Scoreboard", 1, (0, 0, 0))
        start_y = 25
        x = WIDTH - title.get_width() - 10
        self.WINDOW.blit(title, (x, 5))

        ran = min(len(players), 3)
        for count, i in enumerate(sort_players[:ran]):
            text = SCORE_FONT.render(
                str(count + 1) + ". " + str(players[i].name), 1, (0, 0, 0))
            self.WINDOW.blit(text, (x, start_y + count * 20))

        # draw time
        text = TIME_FONT.render(
            "Time: " + self.convert_time(game_time), 1, (0, 0, 0))
        self.WINDOW.blit(text, (10, 10))
        # draw score
        text = TIME_FONT.render("Score: " + str(round(score)), 1, (0, 0, 0))
        self.WINDOW.blit(text, (10, 15 + text.get_height()))


def check_collision(player, foods):
    x = player.x
    y = player.y
    for food in foods:
        bx = food.x
        by = food.y
        dis = math.sqrt((x - bx) ** 2 + (y - by) ** 2)
        if dis <= PLAYER_RADIUS:
            player.increasePlayerScore(1)
            player.addFoodToEatenList(food)
            foods.remove(food)


game = Game()
