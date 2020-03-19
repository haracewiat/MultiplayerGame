import socket
import _pickle as pickle
from gameStateDTO import *
import threading
from queue import LifoQueue

HOST = '127.0.0.1'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buffer = ()
    queue = LifoQueue()
    watching = True

    def __init__(self):
        self.addr = (HOST, PORT)

    def connect(self, name):
        """
        connects to server and returns the id of the client that connected
        :param name: str
        :return: int reprsenting id
        """
        self.sock.connect(self.addr)
        self.sock.send(str.encode(name))
        val = self.sock.recv(BUFFER)
        return int(val.decode())  # can be int because will be an int id

    def disconnect(self):
        self.sock.close()

    def send(self, GameState: GameStateDTO):
        self.sock.sendall(pickle.dumps(GameState))

    def receive(self):
        while True:
            reply = self.sock.recv(BUFFER)
            if not reply:
                break
            try:
                reply = pickle.loads(reply)
                self.queue.put(reply)
            except Exception as e:
                print(e)
            return reply

    def watchGameState(self):
        while self.watching:
            self.receive()
