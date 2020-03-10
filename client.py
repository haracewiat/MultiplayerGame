import socket
import threading
import sys
from game import Game

HOST = '10.4.1.97'  # '18.195.107.195'
PORT = 5378
BUFFER = 4096


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):

        # Connect to the host
        self.connect()

        # Send and receive messages
        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

        self.send()

        # Disconnect
        self.disconnect(thread_receive)

    def receive(self):

        message = b''

        while True:
            data = self.sock.recv(BUFFER)

            if not data:
                break

    def send(self):
        while True:
            self.sock.sendall(input())

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
        except:
            print("Cannot establish connection. Aborting.")
            sys.exit()

        print("Connected to remote host.")

    def reconnect(self):
        print('Connection lost. Trying to reconnect...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def disconnect(self, thread):
        self.sock.shutdown(1)
        thread.join()
        self.sock.close()
        print("Disconnected.")
        sys.exit()


client = Client()
