import socket
from termcolor import colored

class TcpClient:
    """
    Base class for TCP client

    Attributes:
        host (str): host address
        port (int): port number
        buffer_size (int): buffer size
        clientSocket (socket): client socket (communication channel)
    """

    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, name='TCP'):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to server
        self.clientSocket.connect((self.host, self.port))
        print(colored(f'Client {name} is connected to server: {self.clientSocket.getpeername()}', 'green'))

    def receive_message(self):
        """
        Receive message from server and decode it
        :return: decoded message
        """
        return self.clientSocket.recv(self.buffer_size).decode()

    def send_message(self, message):
        """
        Encode message and send it to server
        :param message:
        :return: None
        """
        self.clientSocket.send(message.encode())

    def run(self):
        """
        Main loop for basic echo client
        :return: None
        """
        message = input('|> ')

        while message.lower().strip() != 'exit':
            self.send_message(message)
            response = self.receive_message()

            print(colored(f'Response: {response}', 'blue'))
            message = input('|> ')

        self.send_message(message)

    def __del__(self):
        """
        Dispose client socket when object is destroyed
        :return: None
        """
        print(colored('Client is closed', 'red'))
        self.clientSocket.close()