import socket
from termcolor import colored

class TcpServer:
    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, name='TCP'):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket = None

        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(3)
        print(colored(f'Server {name} is listening on address: {self.serverSocket.getsockname()}', 'green'))

    def accept_client(self):
        self.clientSocket, address = self.serverSocket.accept()
        print(colored(f'Connection from {address}', 'green'))

    def close_client(self):
        self.clientSocket.close()

    def receive_message(self):
        return self.clientSocket.recv(self.buffer_size).decode()

    def send_message(self, message):
        self.clientSocket.send(message.encode())

    def __call__(self, *args, **kwargs):
        self.accept_client()

        while True:
            message = self.receive_message()
            print(colored(f'Send echo message: {message}', 'blue'))

            if message.lower().strip() == 'exit':
                break

            self.send_message(message)

        self.close_client()

    def __del__(self):
        print(colored('Server is closed', 'red'))
        self.serverSocket.close()
