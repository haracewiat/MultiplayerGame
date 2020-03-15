import socket
from _thread import *
import _pickle as pickle
import time
import random
from player import Player
from food import Food
import math

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 5555
SERVER_IP = "127.0.0.1"

FOOD_RADIUS = 10
PLAYER_RADIUS = 18
ROUND_TIME = 600

W, H = 800, 600

try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()

# dynamic variables
players = {}
foods = []
connections = 0
_id = 0
colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255),
          (0, 128, 255), (0, 0, 255), (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128), (128, 128, 128),
          (0, 0, 0)]
start = False

def check_collision(players, foods):
    """
    checks if any of the players have collided with any of the balls

    :param players: a dictonary of players
    :param balls: a list of balls
    :return: None
    """
    for player in players:
        p = players[player]
        x = p.x
        y = p.y
        for food in foods:
            fx = food.x
            fy = food.y
            dis = math.sqrt((x - fx) ** 2 + (y - fy) ** 2)
            if dis <= PLAYER_RADIUS:
                p.increasePlayerScore(1)
                foods.remove(food)

def make_foods(foods, n):
    if len(foods) == (len(players) - 1):
        return
    #print(str(n)+ " balls to create")
    #print(str(len(balls)) +" balls in game")
    for i in range(n):
        while True:
            stop = True
            x = random.randrange(40, W-40)
            y = random.randrange(40, H-40)
            for player in players:
                p = players[player]
                dis = math.sqrt((x - p.x) ** 2 + (y - p.y) ** 2)
                if dis <= PLAYER_RADIUS:
                    stop = False
            if stop:
                break
        food = Food(x,y,random.choice(colors))
        foods.append(food)
    #print(str(len(balls))+ " balls in game after")

def get_start_location(players):
        x = random.randrange(0, W)
        y = random.randrange(0, H)
        return (x, y)

def threaded_client(conn, _id):
    global connections, players, foods, game_time, start

    current_id = _id

    # recieve a name from the client
    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[LOG]", name, "connected to the server.")

    color = random.choice(colors)
    x, y = get_start_location(players)
    player = Player(x,y,color,_id)
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
            data = conn.recv(32)

            if not data:
                break

            data = data.decode("utf-8")
            print("[DATA] Recieved", data, "from client id:", current_id)

            # look for specific commands from recieved data
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players[current_id].x = x
                players[current_id].y = y

                if start:
                    check_collision(players, balls)
                    #player_collision(players)

                #how many balls to create
                if len(players) == 1 and len(balls) == 0:
                    make_foods(foods,1)
                while len(balls) < len(players) - 1:
                    make_foods(foods, 1)
                    print("[GAME] Generating more orbs")
                    if len(balls) == (len(players) - 1):
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