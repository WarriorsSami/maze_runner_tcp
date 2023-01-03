import os
import socket
from termcolor import colored
from dotenv import load_dotenv

load_dotenv()

host = os.environ['HOST']
port = int(os.environ['PORT'])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
    clientSocket.connect((host, port))
    print(colored(f'Client is connected to server: {clientSocket.getpeername()}', 'green'))

    message = input('|> ')

    while message.lower().strip() != 'exit':
        clientSocket.send(message.encode())
        response = clientSocket.recv(1024).decode()

        print(colored(f'Response: {response}', 'blue'))
        message = input('|> ')

    clientSocket.send(message.encode())
    print(colored('Client is closed', 'red'))
    clientSocket.close()
