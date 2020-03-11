import socket
import select
import sys
import pickle
from game_state import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '127.0.0.1'
PORT = 5378
BUFFER = 4096


class Server:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONNECTIONS = dict()
    GAME_STATE = GameStateDTO()

    def __init__(self):

        # Bind
        self.sock.bind((HOST, PORT))
        self.CONNECTIONS['SERVER'] = self.sock

        # Listen for incoming connections
        self.sock.listen()

        # Start threads for accepting and handling connections
        while True:
            read_sockets, write_sockets, error_sockets = select.select(
                self.CONNECTIONS.values(), [], [])

            for connection in read_sockets:
                if connection == self.sock:
                    self.accept_connection()
                else:
                    self.receive(connection)

        self.sock.close()

    def accept_connection(self):
        self.GAME_STATE.update([Player(50, 50), Player(150, 150)])
        connection, address = self.sock.accept()
        connection.send(pickle.dumps(self.GAME_STATE))

    def receive(self, connection):
        while True:
            data = connection.recv(BUFFER)

            if not data:
                self.disconnect(connection)
                return

    def disconnect(self, connection):
        if self.get_value(connection) is not None:
            del self.CONNECTIONS[self.get_value(connection)]
        connection.close()

    def get_value(self, connection):
        for key, value in self.CONNECTIONS.items():
            if value == connection:
                return key
        return None


server = Server()
