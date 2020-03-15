"""
main server script for running agar.io server

can handle multiple/infinite connections on the same
local network
"""
import socket
from _thread import *
import _pickle as pickle
import time
import random
import math
from food import Food
from player import Player

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 5555

BALL_RADIUS = 10
START_RADIUS = 18

ROUND_TIME = 600

MASS_LOSS_TIME = 7

W, H = 1200, 700

HOST_NAME = socket.gethostname()
SERVER_IP = "127.0.0.1"

# try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # listen for connections

print(f"[SERVER] Server Started with local ip {SERVER_IP}")

# dynamic variables
players = {}
foods = []
connections = 0
_id = 0
colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255),
          (0, 128, 255), (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128), (128, 128, 128),
          (0, 0, 0)]
start = False
stat_time = 0
game_time = "Starting Soon"


# FUNCTIONS

def check_collision(players, foods):
    """
    checks if any of the player have collided with any of the foods

    :param players: a dictonary of players
    :param foods: a list of foods
    :return: None
    """

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
                foods.remove(food)

def make_foods(foods, n):
    """
    makes orbs/foods on the screen

    :param foods: a list to add foods/orbs to
    :param n: the amount of foods to make
    :return: None
    """
    if (len(foods) == (len(players) - 1)) and len(players)>1:
        return
    print(str(n)+ " foods to make")
    print(str(len(foods)) +" foods in game")
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
        food = Food(x,y,random.choice(colors))
        foods.append(food)
    print(str(len(foods))+ " foods in game after")

def get_start_location(players):
    """
    picks a start location for a player based on other player
    locations. It wiill ensure it does not spawn inside another player

    :param players: dict
    :return: tuple (x,y)
    """
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


def threaded_client(conn, _id):
    global connections, players, foods, game_time, start
    current_id = _id
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[LOG]", name, "connected to the server.")

    # Setup properties for each new player
    color = colors[current_id]
    x, y = get_start_location(players)
    player = Player(x,y,color,name)
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
    while True:

        if start:
            game_time = round(time.time() - start_time)
            # if the game time passes the round time the game will stop
            if game_time >= ROUND_TIME:
                start = False
        try:
            # Recieve data from client
            data = conn.recv(32)

            if not data:
                break

            data = data.decode("utf-8")
            # print("[DATA] Recieved", data, "from client id:", current_id)

            # look for specific commands from recieved data
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players[current_id].x = x
                players[current_id].y = y

                # only check for collison if the game has started
                if start:
                    check_collision(players, foods)
                    #player_collision(players)

                #how many foods to make
                #print("here "+str(len(players))+" "+str(len(foods)))
                if len(players) == 1 and len(foods) == 0:
                    make_foods(foods,1)
                while len(foods) < len(players) - 1:
                    make_foods(foods, 1)
                    print("[GAME] Generating more orbs")
                    if len(foods) == (len(players) - 1):
                        break

                send_data = pickle.dumps((foods, players, game_time))

            elif data.split(" ")[0] == "id":
                send_data = str.encode(str(current_id))  # if user requests id then send it

            elif data.split(" ")[0] == "jump":
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
    print("[DISCONNECT] Name:", name, ", Client Id:", current_id, "disconnected")

    connections -= 1
    del players[current_id]  # remove client information from players list
    conn.close()  # close connection


# MAINLOOP

# setup level with foods
make_foods(foods, 1)

print("[GAME] Setting up level")
print("[SERVER] Waiting for connections")

# Keep looping to accept new connections
while True:

    host, addr = S.accept()


    print("[CONNECTION] Connected to:", addr)

    # start game when a client on the server computer connects
    if addr[0] == SERVER_IP and not (start):
        start = True
        start_time = time.time()
        print("[STARTED] Game Started")

    # increment connections start new thread then increment ids
    connections += 1
    start_new_thread(threaded_client, (host, _id))
    _id += 1

# when program ends
print("[SERVER] Server offline")
