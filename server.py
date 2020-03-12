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
        print("accepting...")
        connection, address = self.sock.accept()
        self.CONNECTIONS[len(self.CONNECTIONS)] = connection
        connection.send(pickle.dumps(self.GAME_STATE))

    def receive(self, connection):
        print("receiving...")
        while True:
            data = connection.recv(BUFFER)

            if not data:
                break
            else:
                print("received                                             OK")
                self.GAME_STATE = pickle.loads(data)

                print("sending...")
                connection.sendall(pickle.dumps(self.GAME_STATE))
                # self.broadcast()

    def broadcast(self):
        print("broadcasting...")
        # for connection in self.CONNECTIONS.values:
        #    connection.sendall(pickle.dumps(self.GAME_STATE))

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
