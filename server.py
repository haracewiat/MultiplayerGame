import socket
import select
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = '145.108.231.158'
PORT = 5378
NO_CONNECTIONS = 64
BUFFER = 4096


class Server:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONNECTIONS = dict()

    def __init__(self):

        # Bind
        self.sock.bind((HOST, PORT))
        self.CONNECTIONS['SERVER'] = self.sock

        # Listen for incoming connections
        self.sock.listen(NO_CONNECTIONS)

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
        connection, address = self.sock.accept()

    def receive(self, connection):

        while True:
            data = connection.recv(BUFFER)

            if not data:
                # If no data is received, the connection should be closed
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
