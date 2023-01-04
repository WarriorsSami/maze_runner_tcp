import os
from dotenv import load_dotenv
from lib.game.server.multiplexing_game_server import MultiplexingGameServer

load_dotenv()

host = os.environ['HOST']
port = int(os.environ['PORT'])
buffer_size = int(os.environ['BUFFER_SIZE'])
max_connections = int(os.environ['MAX_CONNECTIONS'])

server = MultiplexingGameServer(
    host=host,
    port=port,
    buffer_size=buffer_size,
    max_connections=max_connections,
    name='Maze Runner Multi Client Server')
server.run()
