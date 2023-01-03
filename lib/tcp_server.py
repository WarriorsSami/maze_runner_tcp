import socket
from termcolor import colored

class TcpServer:
    def __init__(self, host='127.0.0.1', port=8889, name='TCP'):
        self.host = host
        self.port = port
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.serverSocket.bind((self.host, self.port))
        self.serverSocket.listen(3)
        print(colored(f'Server {name} is listening on address: {self.serverSocket.getsockname()}', 'green'))

    def __call__(self, *args, **kwargs):
        clientSocket, address = self.serverSocket.accept()
        print(colored(f'Connection from {address}', 'green'))

        while True:
            message = clientSocket.recv(1024).decode()
            print(colored(f'Send echo message: {message}', 'blue'))

            if message.lower().strip() == 'exit':
                break

            response = message.encode()
            clientSocket.send(response)

        clientSocket.close()

    def __del__(self):
        print(colored('Server is closed', 'red'))
        self.serverSocket.close()
