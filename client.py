import socket
import threading
import sys
import pickle
from game_state import GameStateDTO

HOST = '127.0.0.1'
PORT = 5378
BUFFER = 4096*8


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.connect()

    def receive(self):

        print("receiving...")

        data = self.sock.recv(BUFFER)

        if data:
            print("received                                             OK")
            return pickle.loads(data)

    def send(self, GameState: GameStateDTO):
        print("sending")
        self.sock.sendall(pickle.dumps(GameState))

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print("Cannot establish connection. Aborting.")
            return

        print("Connected to remote host.")

    def reconnect(self):
        print('Connection lost. Trying to reconnect...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def disconnect(self, thread):
        self.sock.close()
        print("Disconnected.")
