import os
from dotenv import load_dotenv
from lib.game.server.game_server import GameServer

load_dotenv()

host = os.environ['HOST']
port = int(os.environ['PORT'])
buffer_size = int(os.environ['BUFFER_SIZE'])
max_connections = int(os.environ['MAX_CONNECTIONS'])

server = GameServer(
    host=host,
    port=port,
    buffer_size=buffer_size,
    max_connections=max_connections,
    name='Maze Runner Server'
)
server.run()
