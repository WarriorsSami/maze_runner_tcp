from termcolor import colored

from lib.game.client.game_request import Request
from lib.game.server.game_response import Response
from lib.tcp.tcp_client import TcpClient


def show_menu():
    print(colored('1: Start game', 'yellow'))
    print(colored('2: Stop game', 'yellow'))
    print(colored('h: Help - show menu', 'yellow'))
    print(colored('u: Move up', 'yellow'))
    print(colored('d: Move down', 'yellow'))
    print(colored('l: Move left', 'yellow'))
    print(colored('r: Move right', 'yellow'))
    print(colored('map: Show partial map', 'yellow'))


class GameClient(TcpClient):
    """
    Game Client class derived from TcpClient class.

    It is responsible for sending requests to the server and receiving responses from it.

    Attributes:
        current_request (Request): current request to be sent to the server
        partial_map (list): partial map of the maze from the client's perspective
        character_position (tuple): current position of the character on the map
        steps (int): number of steps taken by the character
    """
    def __init__(self, host='127.0.0.1', port=8889, buffer_size=1024, name='Game Client'):
        super().__init__(host, port, buffer_size, name)
        self.current_request = None
        self.partial_map = []
        self.character_position = None
        self.steps = 0

    def receive_message(self):
        """
        Receives a message from the server and maps it to the Response enum.
        :return: Response enum
        """
        response = super().receive_message()
        match response:
            case 'GAME_STARTED':
                return Response.GAME_STARTED
            case 'GAME_WON':
                return Response.GAME_WON
            case 'GAME_OVER':
                return Response.GAME_OVER
            case 'WALL_COLLISION':
                return Response.WALL_COLLISION
            case 'OK':
                return Response.OK
            case 'ERROR':
                return Response.ERROR
            case _:
                return Response.UNKNOWN

    def run(self):
        """
        Main loop of the client.
        """

        # user prompt
        show_menu()
        message = input('|> ')
        message = message.lower().strip()

        while True:
            try:
                # for distinguishing between the requests (which are sent to the server)
                # and the commands (which are tasks executed locally by the client)
                execute_client_side_command = False

                # map the user input to the Request enum
                match message:
                    case '1':
                        self.current_request = Request.START
                    case '2':
                        # stop the game session but only after sending the STOP request to the server
                        self.current_request = Request.STOP
                        break
                    case 'h':
                        show_menu()
                        execute_client_side_command = True
                    case 'u':
                        self.current_request = Request.UP
                    case 'd':
                        self.current_request = Request.DOWN
                    case 'l':
                        self.current_request = Request.LEFT
                    case 'r':
                        self.current_request = Request.RIGHT
                    case 'map':
                        self.print_partial_map()
                        execute_client_side_command = True
                    case _:
                        self.current_request = Request.UNKNOWN

                # if the user input is a request, send it to the server
                if self.current_request != Request.UNKNOWN and not execute_client_side_command:
                    self.send_message(self.current_request)

                    # receive the response from the server
                    response = self.receive_message()
                    print(colored(f'Response: {response}', 'blue'))

                    # map the response to the Response enum
                    match response:
                        case Response.GAME_STARTED:
                            # initialize the character's position and the partial map
                            self.init_character()

                            print(colored('Game started! Now you can start controlling your character!', 'green'))
                        case Response.GAME_WON:
                            print(colored('You won! Congratulations!', 'green'))
                            print(colored(f'You managed to exit the maze in {self.steps} steps!', 'green'))

                            print(colored('\nYour game status:', 'yellow'))
                            self.register_exit_position()
                            self.print_partial_map()

                            print(colored('\nChoose what to do next:', 'yellow'))
                            show_menu()

                            self.clear_map_state()
                        case Response.GAME_OVER:
                            print(colored('You lost as you encountered a monster! Try again!', 'red'))

                            print(colored('\nYour game status:', 'yellow'))
                            self.register_monster_position()
                            self.print_partial_map()

                            print(colored('\nChoose what to do next:', 'yellow'))
                            show_menu()

                            self.clear_map_state()
                        case Response.OK:
                            # update the character's position and the partial map
                            print(colored('The move was executed successfully!', 'green'))
                            self.update_character_position()
                        case Response.WALL_COLLISION:
                            # mark a new wall on the partial map
                            print(colored('You cannot move there! You\'ve just hit a wall!', 'red'))
                            self.register_wall_position()
                        case Response.ERROR:
                            print(colored('Something went wrong! Try again!', 'red'))
                # an unknown request was intercepted
                elif self.current_request == Request.UNKNOWN and not execute_client_side_command:
                    print(colored('Unknown command! Try something else!', 'red'))

                # get the next user input
                message = input('|> ')
                message = message.lower().strip()

            except Exception as e:
                print(colored(f'Exception occurred: {e}', 'red'))

        # send the stop request to the server
        self.send_message(self.current_request)

    def init_character(self):
        """
        Initializes the character's position and the partial map.
        """

        # send a request to the server to get the partial map's size and the character's position
        self.send_message(Request.SEND_PLAYER_DETAILS)

        # receive the response from the server
        response = super().receive_message()
        print(colored(f'Response: {response}', 'blue'))

        # extract the character's position
        character_data = response.split(' ')
        self.character_position = (int(character_data[0]), int(character_data[1]))

        # extract the partial map size and initialize the partial map
        (map_width, map_height) = (int(character_data[2]), int(character_data[3]))
        self.partial_map = [['?' for _ in range(map_width)] for _ in range(map_height)]

    def print_partial_map(self):
        if len(self.partial_map) == 0:
            print(colored('You don\'t have a map yet! '
                          'Please initiate a new game session with the server first of all!', 'red'))
            return

        self.partial_map[self.character_position[0]][self.character_position[1]] = 'J'

        for row in self.partial_map:
            for cell in row:
                match cell:
                    case '?':
                        print(colored(cell, 'yellow'), end=' ')
                    case 'J':
                        print(colored(cell, 'green'), end=' ')
                    case '#':
                        print(colored(cell, 'blue'), end=' ')
                    case 'M':
                        print(colored(cell, 'red'), end=' ')
                    case 'E':
                        print(colored(cell, 'cyan'), end=' ')
                    case _:
                        print(colored(cell, 'white'), end=' ')
            print()

        self.partial_map[self.character_position[0]][self.character_position[1]] = ' '

    def update_character_position(self):
        """
        Updates the character's position and the partial map based on the last move (stored in self.current_request).
        """

        self.steps += 1
        self.partial_map[self.character_position[0]][self.character_position[1]] = ' '

        match self.current_request:
            case Request.UP:
                self.character_position = (self.character_position[0] - 1, self.character_position[1])
            case Request.DOWN:
                self.character_position = (self.character_position[0] + 1, self.character_position[1])
            case Request.LEFT:
                self.character_position = (self.character_position[0], self.character_position[1] - 1)
            case Request.RIGHT:
                self.character_position = (self.character_position[0], self.character_position[1] + 1)

    def register_wall_position(self):
        """
        Registers the position of a wall on the partial map based on the last move (stored in self.current_request).
        """

        self.steps += 1
        match self.current_request:
            case Request.UP:
                self.partial_map[self.character_position[0] - 1][self.character_position[1]] = '#'
            case Request.DOWN:
                self.partial_map[self.character_position[0] + 1][self.character_position[1]] = '#'
            case Request.LEFT:
                self.partial_map[self.character_position[0]][self.character_position[1] - 1] = '#'
            case Request.RIGHT:
                self.partial_map[self.character_position[0]][self.character_position[1] + 1] = '#'

    def clear_map_state(self):
        self.partial_map = []
        self.steps = 0
        self.character_position = None

    def register_monster_position(self):
        """
        Registers the position of a monster on the partial map based on the last move (stored in self.current_request).
        """

        match self.current_request:
            case Request.UP:
                self.partial_map[self.character_position[0] - 1][self.character_position[1]] = 'M'
            case Request.DOWN:
                self.partial_map[self.character_position[0] + 1][self.character_position[1]] = 'M'
            case Request.LEFT:
                self.partial_map[self.character_position[0]][self.character_position[1] - 1] = 'M'
            case Request.RIGHT:
                self.partial_map[self.character_position[0]][self.character_position[1] + 1] = 'M'

    def register_exit_position(self):
        """
        Registers the position of the exit on the partial map based on the last move (stored in self.current_request).
        """

        match self.current_request:
            case Request.UP:
                self.partial_map[self.character_position[0] - 1][self.character_position[1]] = 'E'
            case Request.DOWN:
                self.partial_map[self.character_position[0] + 1][self.character_position[1]] = 'E'
            case Request.LEFT:
                self.partial_map[self.character_position[0]][self.character_position[1] - 1] = 'E'
            case Request.RIGHT:
                self.partial_map[self.character_position[0]][self.character_position[1] + 1] = 'E'
