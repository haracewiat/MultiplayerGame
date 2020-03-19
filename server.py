import socket
from _thread import *
import _pickle as pickle
import time
import random
import math

import pygame

from food import Food
from player import Player
from constants import colors
from gameStateDTO import *

players = {}
foods = []
connections = 0
_id = 0
food_id = 0
game_time = "Starting Soon"
start = False
start_time = 0

HOST = '127.0.0.1'
PORT = 5378

BALL_RADIUS = 10
START_RADIUS = 18
ROUND_TIME = 600
W, H = 1200, 700


class Server:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONNECTIONS = dict()

    def __init__(self):

        self.sock.bind((HOST, PORT))
        self.sock.listen()

        print(f"[SERVER] Server Started with local ip {HOST}")

        # Keep looping to accept new connections
        while True:

            host, addr = self.sock.accept()

            print("[CONNECTION] Connected to:", addr)

            # start game when a client on the server computer connects
            global start, start_time
            if addr[0] == HOST and not (start):
                start = True
                start_time = time.time()
                print("[STARTED] Game Started")

            # increment connections start new thread then increment ids
            global connections, _id

            connections += 1
            #make_foods(foods, 1)
            start_new_thread(self.player_thread, (host, _id))
            _id += 1

        self.sock.close()

        # when program ends
        print("[SERVER] Server offline")

    def player_thread(self, conn, _id):
        global connections, players, foods, game_time, start
        current_id = _id
        data = conn.recv(16)
        name = data.decode("utf-8")
        print("[LOG]", name, "connected to the server.")

        # Setup properties for each new player
        color = colors[current_id]
        x, y = get_start_location(players)
        player = Player(x, y, color, name, current_id)
        players[current_id] = player

        # pickle data and send initial info to clients
        conn.send(str.encode(str(current_id)))

        # server will recieve basic commands from client
        # it will send back all of the other clients info
        '''
        commands start with:
        move
        jump
        get
        id - returns id of client
        '''
        clock = pygame.time.Clock()
        while True:
            clock.tick(10)

            if start:
                game_time = round(time.time() - start_time)
                # if the game time passes the round time the game will stop
                if game_time >= ROUND_TIME:
                    start = False
            try:
                # Recieve data from client
                data = conn.recv(1024)

                if not data:
                    break

                # print("[DATA] Recieved", data, "from client id:", current_id)

                # look for specific commands from recieved data
                gameState = pickle.loads(data)
                if gameState.command == 'move':
                    players[current_id].x = gameState.x
                    players[current_id].y = gameState.y
                    players[current_id].playerScore = gameState.score
                    players[current_id].playerVelocity = gameState.velocity

                    #print(str(score) + " " + str(velocity))

                    # only check for collison if the game has started
                    if start:
                        check_collision(players, foods)
                        # player_collision(players)

                    # how many foods to make
                    #print("here "+str(len(players))+" "+str(len(foods)))
                    while len(foods) < len(players) - 1:
                        make_foods(foods, 1)
                        print("[GAME] Generating more orbs")
                        if len(foods) == (len(players) - 1):
                            break

                    send_data = pickle.dumps((foods, players, game_time))

                elif gameState.command == 'id':
                    # if user requests id then send it
                    send_data = str.encode(str(current_id))

                elif gameState.command == 'jump':
                    send_data = pickle.dumps((foods, players, game_time))
                else:
                    # any other command just send back list of players
                    send_data = pickle.dumps((foods, players, game_time))

                # send data back to clients
                conn.send(send_data)

            except Exception as e:
                print(e)
                break  # if an exception has been reached disconnect client

            time.sleep(0.001)

        # When user disconnects
        print("[DISCONNECT] Name:", name,
              ", Client Id:", current_id, "disconnected")

        connections -= 1
        del players[current_id]  # remove client information from players list
        conn.close()  # close connection


# Game engine functions
def check_collision(players, foods):
    for player in players:
        p = players[player]
        x = p.x
        y = p.y
        for food in foods:
            bx = food.x
            by = food.y
            dis = math.sqrt((x - bx) ** 2 + (y - by) ** 2)
            if dis <= START_RADIUS:
                p.increasePlayerScore(1)
                p.addFoodToEatenList(food)
                foods.remove(food)
                make_foods(foods, 1)


def make_foods(foods, n):
    global food_id
    if (len(foods) == (len(players) - 1)) and len(players) > 1:
        return
    print(str(n) + " foods to make")
    print(str(len(foods)) + " foods in game")
    for i in range(n):
        while True:
            stop = True
            x = random.randrange(40, W-40)
            y = random.randrange(40, H-40)
            for player in players:
                p = players[player]
                dis = math.sqrt((x - p.x) ** 2 + (y - p.y) ** 2)
                if dis <= START_RADIUS:
                    stop = False
            if stop:
                break
        if (len(foods) == (len(players) - 1)) and len(players) > 1:
            return
        else:
            food = Food(x, y, random.choice(colors), food_id)
            food_id += 1
            foods.append(food)
    print(str(len(foods)) + " foods in game after")


def get_start_location(players):
    while True:
        stop = True
        x = random.randrange(0, W)
        y = random.randrange(0, H)
        for player in players:
            p = players[player]
            dis = math.sqrt((x - p.x) ** 2 + (y - p.y) ** 2)
            if dis <= START_RADIUS:
                stop = False
                break
        if stop:
            break
    return (x, y)


server = Server()
