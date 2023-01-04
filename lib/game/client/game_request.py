from enum import Enum

class Request(Enum):
    START = 1,
    STOP = 2,
    UP = 3,
    DOWN = 4,
    LEFT = 5,
    RIGHT = 6,
    SHOW_PARTIAL_MAP = 7,

    def __str__(self):
        return self.name