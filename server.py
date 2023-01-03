import os
from lib.tcp_server import TcpServer
from dotenv import load_dotenv

load_dotenv()

host = os.environ['HOST']
port = int(os.environ['PORT'])

tcpServer = TcpServer(host, port)
tcpServer()
