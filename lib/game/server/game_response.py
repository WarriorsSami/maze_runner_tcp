from enum import Enum

class Response(Enum):
    OK = 1,
    WALL_COLLISION = 2,
    GAME_OVER = 3,
    GAME_WIN = 4,
    ERROR = 5,

    def __str__(self):
        return self.name