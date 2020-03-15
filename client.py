import socket
import pickle as pickle
import threading

BUFFER = 4096*4

class Client:

    global data_buffer

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "127.0.0.1"
        self.port = 5555
        self.addr = (self.host, self.port)

    def connect(self):
        self.client.connect(self.addr)

    def disconnect(self):
        self.client.close()

    def start_receiving_thread(self):
        thread_receive = threading.Thread(target=self.receive)
        thread_receive.start()

    def receive(self):
        while True:
            data = self.client.recv(BUFFER)
            try:
                reply = pickle.loads(data)
            except Exception as e:
                print(e)
            self.data_buffer = reply

    def get_data_buffer(self):
        return self.data_buffer

    def sendName(self, name):
        self.client.send(str.encode(name))
        val = self.client.recv(8)
        return int(val.decode())

    def sendData(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)