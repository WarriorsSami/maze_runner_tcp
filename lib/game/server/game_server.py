from termcolor import colored

from lib.game.client.game_request import Request
from lib.game.server.game_response import Response
from lib.map.map_entity import MapEntity
from lib.map.random_generator import get_random_map
from lib.tcp.tcp_server import TcpServer


def map_request_to_enum(request):
    """
    Map request to Request enum
    :param request:
    :return: Request enum
    """
    match request:
        case 'START':
            return Request.START
        case 'STOP':
            return Request.STOP
        case 'UP':
            return Request.UP
        case 'DOWN':
            return Request.DOWN
        case 'LEFT':
            return Request.LEFT
        case 'RIGHT':
            return Request.RIGHT
        case 'SEND_PLAYER_DETAILS':
            return Request.SEND_PLAYER_DETAILS
        case value:
            print(colored(f'Unknown request: {value}', 'red'))
            return Request.UNKNOWN


class GameServer(TcpServer):
    """
    Game Server class derived from TcpServer class.

    It is responsible for handling game requests from client and sending game responses to client.

    Attributes:
        game_map (Map): game map
    """
    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, max_connections=3, name='Game Server'):
        super().__init__(host, port, buffer_size, max_connections, name)
        self.game_map = None

    def receive_message(self):
        """
        Receive message from client, decode it and map it to Request enum
        :return: Request enum
        """
        request = super().receive_message()
        print(colored(f'Request received from client: {request}', 'blue'))

        return map_request_to_enum(request)

    def send_message(self, message):
        """
        log message and send it to client
        :param message: message to send
        """
        print(colored(f'Sending message to client: {message}', 'green'))
        super().send_message(message)

    def run(self):
        """
        Main loop for game server
        """

        # wait for client to connect
        self.accept_client()

        while True:
            try:
                # receive request from client
                request = self.receive_message()

                # handle request
                match request:
                    case Request.START:
                        # initialize game map and print it on the server terminal
                        self.init_game_map()
                        self.game_map.print_map()

                        self.send_message(Response.GAME_STARTED)
                    case Request.STOP:
                        # stop the game
                        break
                    case Request.SEND_PLAYER_DETAILS:
                        # send player details to client
                        player_details = self.game_map.get_player_details()
                        player_details = f"{player_details[0][0]} {player_details[0][1]} {player_details[1][0]} {player_details[1][1]}"
                        self.send_message(player_details)
                    case Request.UP:
                        self.try_to_move_player(-1, 0)
                    case Request.DOWN:
                        self.try_to_move_player(1, 0)
                    case Request.LEFT:
                        self.try_to_move_player(0, -1)
                    case Request.RIGHT:
                        self.try_to_move_player(0, 1)
                    case Request.UNKNOWN:
                        self.send_message(Response.ERROR)

            except Exception as e:
                print(colored(f'Error: {e}', 'red'))
                self.send_message(Response.ERROR)

    def init_game_map(self):
        """
        Initialize game map with random map
        """
        self.game_map = get_random_map()

    def try_to_move_player(self, dx, dy):
        """
        Try to move player in given direction and send response to client
        :param dx: x direction
        :param dy: y direction
        """

        # if the move is possible
        if self.game_map.is_move_possible(dx, dy):
            # move player
            self.game_map.set_player_position(
                (
                    self.game_map.player_position[0] + dx,
                    self.game_map.player_position[1] + dy
                )
            )
            # send ok response to client
            self.send_message(Response.OK)

        # if the next position is blocked
        elif self.game_map.is_in_matrix(
                self.game_map.player_position[0] + dx,
                self.game_map.player_position[1] + dy
        ):
            # get its entity type
            value = self.game_map.get_value_at(
                (
                    self.game_map.player_position[0] + dx,
                    self.game_map.player_position[1] + dy
                )
            )

            # send response to client based on entity type
            match value:
                case MapEntity.WALL:
                    self.send_message(Response.WALL_COLLISION)
                case MapEntity.EXIT:
                    self.send_message(Response.GAME_WON)
                case MapEntity.MONSTER:
                    self.send_message(Response.GAME_OVER)
                case _:
                    self.send_message(Response.ERROR)
        # invalid game state reached
        else:
            self.send_message(Response.ERROR)
