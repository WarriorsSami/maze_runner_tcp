from enum import Enum

class Request(Enum):
    """
    Enum for representing game requests from client to server:

    START - start the game
    STOP - stop the game
    UP - move the player up
    DOWN - move the player down
    LEFT - move the player left
    RIGHT - move the player right
    SEND_PLAYER_DETAILS - send player details to client (player position, matrix size)
    UNKNOWN - unknown request
    """

    START = 1,
    STOP = 2,
    UP = 3,
    DOWN = 4,
    LEFT = 5,
    RIGHT = 6,
    SEND_PLAYER_DETAILS = 7,
    UNKNOWN = 8,

    def __str__(self):
        return self.name

    def encode(self):
        return self.name.encode()
