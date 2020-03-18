import socket
import _pickle as pickle
from gameStateDTO import *
#import threading

HOST = '127.0.0.1'
PORT = 5378


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        val = self.sock.recv(8)
        return int(val.decode())  # can be int because will be an int id

    def disconnect(self):
        """
        disconnects from the server
        :return: None
        """
        self.sock.close()

    def send(self, GameState: GameStateDTO):
        """
        sends information to the server

        :param data: str
        :param pick: boolean if should pickle or not
        :return: str
        """
        self.sock.sendall(pickle.dumps(GameState))

        # try:
        #     if pick:
        #         self.sock.send(pickle.dumps(data))
        #     else:
        #         self.sock.send(str.encode(data))
        # except socket.error as e:
        #     print(e)

    def receive(self):
        reply = self.sock.recv(2048 * 4)
        try:
            reply = pickle.loads(reply)
            print(reply)
        except Exception as e:
            print(e)
        return reply
