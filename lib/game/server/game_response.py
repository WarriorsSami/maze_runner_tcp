from enum import Enum

class Response(Enum):
    """
    Enum for representing game responses from server to client:

    GAME_STARTED - game started
    GAME_STOPPED - game stopped
    ERROR - server-side error
    OK - the player can move
    UNKNOWN - unknown response
    WALL_COLLISION - the player hit a wall
    """

    OK = 1,
    WALL_COLLISION = 2,
    GAME_STARTED = 3,
    GAME_WON = 4,
    GAME_OVER = 5,
    ERROR = 6,
    UNKNOWN = 7,

    def __str__(self):
        return self.name

    def encode(self):
        return self.name.encode()