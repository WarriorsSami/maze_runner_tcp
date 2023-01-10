from termcolor import colored
import threading as th

from lib.game.client.game_request import Request
from lib.game.server.game_response import Response
from lib.game.server.game_server import GameServer, map_request_to_enum
from lib.map.map_entity import MapEntity
from lib.map.random_generator import get_random_map


class MultiplexingGameServer(GameServer):
    """
    Multiplexing Game Server handles multiple clients

    Attributes:
        client_sessions: dictionary of addr: (socket, game_map)
    """

    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, max_connections=3, name='Multi Client Game Server'):
        super().__init__(host, port, buffer_size, max_connections, name)
        # dictionary of addr: (socket, game_map)
        self.client_sessions = {}

    def accept_client(self):
        """
        Accept client connection, create a new thread for it and add it to client_sessions
        """
        client_socket, address = self.server_socket.accept()
        print(colored(f'Connection from {address}', 'green'))
        self.client_sessions[address] = (client_socket, None)
        th.Thread(target=self.handle_client, args=(client_socket, address)).start()

    def receive_message_from(self, client_socket, address):
        # check if client socket is not closed
        if client_socket.fileno() == -1:
            self.dispose_client_session(address)
            return

        request = client_socket.recv(self.buffer_size).decode()
        print(colored(f'Request received from client {address}: {request}', 'blue'))

        return map_request_to_enum(request)

    def send_message_to(self, client_socket, address, message):
        """
        log message and send it to client
        :param address:
        :param client_socket:
        :param message: message to send
        """
        if client_socket.fileno() == -1:
            self.dispose_client_session(address)
            return

        print(colored(f'Sending message to client {address}: {message}', 'green'))
        client_socket.send(message.encode())

    def get_map_for(self, address):
        return self.client_sessions[address][1]

    def init_game_map_for(self, address):
        self.client_sessions[address] = (self.client_sessions[address][0], get_random_map())

    def try_to_move_player_for(self, client_socket, address, dx, dy):
        """
        Try to move player in given direction and send response to client
        :param address:
        :param client_socket:
        :param dx: x direction
        :param dy: y direction
        """

        game_map = self.get_map_for(address)

        # if the move is possible
        if game_map.is_move_possible(dx, dy):
            # move player
            game_map.set_player_position(
                (
                    game_map.player_position[0] + dx,
                    game_map.player_position[1] + dy
                )
            )
            # send ok response to client
            self.send_message_to(client_socket, address, Response.OK)

        # if the next position is blocked
        elif game_map.is_in_matrix(
                game_map.player_position[0] + dx,
                game_map.player_position[1] + dy
        ):
            # get its entity type
            value = game_map.get_value_at(
                (
                    game_map.player_position[0] + dx,
                    game_map.player_position[1] + dy
                )
            )

            # send response to client based on entity type
            match value:
                case MapEntity.WALL:
                    self.send_message_to(client_socket, address, Response.WALL_COLLISION)
                case MapEntity.EXIT:
                    self.send_message_to(client_socket, address, Response.GAME_WON)
                case MapEntity.MONSTER:
                    self.send_message_to(client_socket, address, Response.GAME_OVER)
                case _:
                    self.send_message_to(client_socket, address, Response.ERROR)
        # invalid game state reached
        else:
            self.send_message_to(client_socket, address, Response.ERROR)

    def handle_client(self, client_socket, address):
        while True:
            try:
                # receive request from client
                request = self.receive_message_from(client_socket, address)

                # handle request
                match request:
                    case Request.START:
                        # initialize game map and print it on the server terminal
                        self.init_game_map_for(address)
                        self.get_map_for(address).print_map()

                        self.send_message_to(client_socket, address, Response.GAME_STARTED)
                    case Request.STOP:
                        self.dispose_client_session(address)
                        break
                    case Request.SEND_PLAYER_DETAILS:
                        # send player details to client
                        player_details = self.get_map_for(address).get_player_details()
                        player_details = f"{player_details[0][0]} {player_details[0][1]} {player_details[1][0]} {player_details[1][1]}"
                        self.send_message_to(client_socket, address, player_details)
                    case Request.UP:
                        self.try_to_move_player_for(client_socket, address, -1, 0)
                    case Request.DOWN:
                        self.try_to_move_player_for(client_socket, address, 1, 0)
                    case Request.LEFT:
                        self.try_to_move_player_for(client_socket, address, 0, -1)
                    case Request.RIGHT:
                        self.try_to_move_player_for(client_socket, address, 0, 1)
                    case Request.UNKNOWN:
                        self.send_message_to(client_socket, address, Response.ERROR)

            except Exception as e:
                print(colored(f'Error: {e}', 'red'))
                self.send_message_to(client_socket, address, Response.ERROR)

    def run(self):
        # accept client connections
        while True:
            self.accept_client()

    def __del__(self):
        # close all client sockets and server socket
        super().__del__()
        for client_session in self.client_sessions.values():
            client_session[0].close()

    def dispose_client_session(self, address):
        # remove client session from client_sessions
        self.client_sessions.pop(address)
