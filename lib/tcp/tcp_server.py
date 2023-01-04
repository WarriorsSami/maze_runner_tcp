import socket
from termcolor import colored

class TcpServer:
    """
    Base class for TCP server

    Attributes:
        host (str): host address
        port (int): port number
        buffer_size (int): buffer size
        server_socket (socket): server socket (handshaking/welcoming channel)
        client_socket (socket): client socket (communication channel)
    """

    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, max_connections=3, name='TCP'):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket = None

        # Bind server to address
        self.server_socket.bind((self.host, self.port))
        # Listen for incoming connections
        self.server_socket.listen(max_connections)
        print(colored(f'Server {name} is listening on address: {self.server_socket.getsockname()}', 'green'))

    def accept_client(self):
        """
        Accept client connection
        :return: None
        """
        self.client_socket, address = self.server_socket.accept()
        print(colored(f'Connection from {address}', 'green'))

    def close_client(self):
        """
        Dispose client socket
        :return: None
        """
        self.client_socket.close()

    def receive_message(self):
        """
        Receive message from client and decode it
        :return: decoded message
        """
        return self.client_socket.recv(self.buffer_size).decode()

    def send_message(self, message):
        """
        Encode message and send it to client
        :param message:
        :return: None
        """
        self.client_socket.send(message.encode())

    def run(self):
        """
        Main loop for basic echo server
        :return: None
        """
        self.accept_client()

        while True:
            message = self.receive_message()
            print(colored(f'Send echo message: {message}', 'blue'))

            if message.lower().strip() == 'exit':
                break

            self.send_message(message)

        self.close_client()

    def __del__(self):
        """
        Dispose server socket when object is destroyed
        :return: None
        """
        print(colored('Server is closed', 'red'))
        self.server_socket.close()
