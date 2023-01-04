import os
from dotenv import load_dotenv
from lib.game.client.game_client import GameClient

load_dotenv()

host = os.environ['HOST']
port = int(os.environ['PORT'])
buffer_size = int(os.environ['BUFFER_SIZE'])

client = GameClient(host=host, port=port, buffer_size=buffer_size, name='Maze Runner Client')
client.run()
