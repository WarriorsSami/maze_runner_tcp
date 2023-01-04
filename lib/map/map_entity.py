from enum import Enum

def to_map_entity(value):
    match value:
        case '.':
            return MapEntity.EMPTY_CELL
        case '#':
            return MapEntity.WALL
        case 'J':
            return MapEntity.PLAYER
        case 'M':
            return MapEntity.MONSTER
        case 'E':
            return MapEntity.EXIT
        case _:
            raise ValueError(f'Invalid value: {value}')

class MapEntity(Enum):
    EMPTY_CELL = '.',
    WALL = '#',
    PLAYER = 'J',
    MONSTER = 'M',
    EXIT = 'E',

    def __str__(self):
        return self.value

    def is_empty(self):
        return self == MapEntity.EMPTY_CELL

    def is_wall(self):
        return self == MapEntity.WALL

    def is_player(self):
        return self == MapEntity.PLAYER

    def is_monster(self):
        return self == MapEntity.MONSTER

    def is_exit(self):
        return self == MapEntity.EXIT