import contextlib

with contextlib.redirect_stdout(None):
    import pygame
from client import Client
from food import Food
from player import Player
import random
import os
import sys

PLAYER_RADIUS = 10
START_VEL = 9
FOOD_RADIUS = 5

W, H = 800, 600

COLORS = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255),
          (0, 128, 255), (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128), (128, 128, 128),
          (0, 0, 0)]

players = {}
balls = []

def draw_game(players, foods):
    CANVAS.fill((255, 255, 255))
    for food in foods:
        pygame.draw.circle(CANVAS, food.color, (food.x,food.y), FOOD_RADIUS)
    for player in players:
        pygame.draw.circle(CANVAS, player.color, (player.x,player.y), PLAYER_RADIUS)


def main(name):
    global players
    client = Client()
    client.connect()
    id = client.sendName(name)
    client.sendData("get")
    client.start_receiving_thread()

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        p = players[id]
        vel = START_VEL
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            if p.x - vel >= 0:
                p.x = p.x - vel

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            if p.x + vel <= W:
                p.x = p.x + vel

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if p.y - vel >= 0:
                p.y = p.y - vel

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if p.y + vel <= H:
                p.y = p.y + vel

        data = "move" + str(p.x) + " " + str(p.y)
        client.sendData(data)



    pass


CANVAS = pygame.display.set_mode((W, H))

main(sys.argv[1])