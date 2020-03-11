import socket
import threading
import sys
import pickle
import game

HOST = '127.0.0.1'
PORT = 5378
BUFFER = 4096*8


class Client:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    GAME_STATE = None

    def __init__(self):

        game.Game()

        # Connect to the host
        self.connect()

        # Send and receive messages
        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

        self.send()

        # Disconnect
        self.disconnect(thread_receive)

    def receive(self):
        while True:
            data = self.sock.recv(BUFFER)

            if not data:
                break
            else:
                self.GAME_STATE = pickle.loads(data)
                print(self.GAME_STATE)

    def send(self):
        while True:
            self.sock.sendall(bytes(input(), 'utf-8'))

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
