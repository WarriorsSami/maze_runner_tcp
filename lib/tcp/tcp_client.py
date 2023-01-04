import socket
from termcolor import colored

class TcpClient:
    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, name='TCP'):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.clientSocket.connect((self.host, self.port))
        print(colored(f'Client {name} is connected to server: {self.clientSocket.getpeername()}', 'green'))

    def receive_message(self):
        return self.clientSocket.recv(self.buffer_size).decode()

    def send_message(self, message):
        self.clientSocket.send(message.encode())

    def __call__(self, *args, **kwargs):
        message = input('|> ')

        while message.lower().strip() != 'exit':
            self.send_message(message)
            response = self.receive_message()

            print(colored(f'Response: {response}', 'blue'))
            message = input('|> ')

        self.send_message(message)

    def __del__(self):
        print(colored('Client is closed', 'red'))
        self.clientSocket.close()