import os
from dotenv import load_dotenv
from lib.game.server.game_server import GameServer

load_dotenv()

host = os.environ['HOST']
port = int(os.environ['PORT'])
buffer_size = int(os.environ['BUFFER_SIZE'])

server = GameServer(host=host, port=port, buffer_size=buffer_size, name='Maze Runner Server')
server()
