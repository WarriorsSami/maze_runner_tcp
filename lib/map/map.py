from termcolor import colored
from lib.map.map_entity import MapEntity, to_map_entity


def get_manhattan_distance(position1, position2):
    """
    Returns the Manhattan distance between two positions
    :param position1: tuple
    :param position2: tuple
    :return: int
    """

    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


class Map:
    """
    Class for representing a Game Map

    Attributes
    ----------
    map_file_path : str (the map template file path)
    map_size : tuple (the map size)
    entity_map : list (the map entity representation)
    bfs_map : list (the BFS map used for marking the player's valid positions)
    player_position : tuple (the player's position)
    monster_position : tuple (the monster's position)
    """

    def __init__(self, map_file_path):
        self.map_file_path = map_file_path
        self.map_size = (0, 0)
        self.entity_map = []
        self.bfs_map = []

        self.read_map()
        self.mark_exit_positions()

        self.player_position = None
        self.monster_position = None

    def get_player_details(self):
        return self.player_position, self.map_size

    def read_map(self):
        with open(self.map_file_path, 'r') as file:
            map_value = [list(line.strip()) for line in file]
            # convert map to entity map (e.g. ' ' -> MapEntity.EMPTY_CELL) using python's map function
            self.entity_map = list(map(lambda row: list(map(to_map_entity, row)), map_value))
            self.map_size = (len(map_value), len(map_value[0]))

    def mark_exit_positions(self):
        for row in range(self.map_size[0]):
            for col in range(self.map_size[1]):
                if self.entity_map[row][col] == MapEntity.EMPTY_CELL and self.is_edge_position((row, col)):
                    self.entity_map[row][col] = MapEntity.EXIT

    def get_player_valid_positions(self):
        """
        Returns a list of all valid positions (empty cells that are reachable from an exit) for the player
        using a BFS traversal
        :return: list of tuples
        """

        # mark all exits as 0 using python's map function
        bfs_map = list(map(lambda _row: list(map(lambda _cell: 0 if _cell == MapEntity.EXIT else -1, _row)), self.entity_map))

        # get the list of all exit positions using python's filter function
        exit_list = list(filter(lambda position: self.get_value_at(position) == MapEntity.EXIT, self.get_all_positions()))

        # add the exit positions into a bfs queue
        bfs_queue = exit_list.copy()

        # bfs
        while len(bfs_queue) > 0:
            current_position = bfs_queue.pop(0)
            (row, col) = current_position
            current_value = bfs_map[row][col]

            for next_position in self.get_next_positions(current_position):
                (next_row, next_col) = next_position

                if bfs_map[next_row][next_col] == -1:
                    bfs_map[next_row][next_col] = current_value + 1
                    bfs_queue.append(next_position)

        # store the BFS map to be used later in marking the monster's valid positions
        self.bfs_map = bfs_map

        # collect all values greater than 2 (i.e. reachable from an exit via at least 3 moves)
        return list(filter(lambda position: bfs_map[position[0]][position[1]] > 2, self.get_all_positions()))

    def get_monster_valid_positions(self):
        """
        Returns all positions that are reachable from the player's position at a maximum of 3 moves
        and are not walls or exits
        :return: list of tuples
        """

        valid_positions = list(
            filter(
                lambda _position:
                self.bfs_map[_position[0]][_position[1]] > 0
                and get_manhattan_distance(self.player_position, _position) == 3
                and self.entity_map[_position[0]][_position[1]] != MapEntity.WALL
                and self.entity_map[_position[0]][_position[1]] != MapEntity.EXIT,
                self.get_all_positions()
            )
        )

        # filter out monster positions that obstruct the player's path to an exit
        return list(filter(lambda _position: self.is_exit_reachable_with_monster(_position), valid_positions))

    def is_exit_reachable_with_monster(self, monster_position):
        """
        Checks if any exit is reachable from the player position when the monster is at the given position
        :param monster_position:
        :return: bool
        """

        # mark the monster position as a wall in the entity map
        self.set_entity_position(monster_position, MapEntity.WALL)

        # mark player position as 0
        bfs_map = list(map(lambda _row: list(map(lambda _cell: 0 if _cell == MapEntity.PLAYER else -1, _row)), self.entity_map))

        # add the player position into a bfs queue
        bfs_queue = [self.player_position]

        # bfs
        while len(bfs_queue) > 0:
            current_position = bfs_queue.pop(0)
            (row, col) = current_position
            current_value = bfs_map[row][col]

            for next_position in self.get_next_positions(current_position):
                (next_row, next_col) = next_position

                if bfs_map[next_row][next_col] == -1:
                    bfs_map[next_row][next_col] = current_value + 1
                    bfs_queue.append(next_position)
                    if self.entity_map[next_row][next_col] == MapEntity.EXIT:
                        # if an exit is reachable, return True (don't forget to unmark the monster position)
                        self.set_entity_position(monster_position, MapEntity.EMPTY_CELL)
                        return True

        # if no exit is reachable, return False (don't forget to unmark the monster position)
        self.set_entity_position(monster_position, MapEntity.EMPTY_CELL)
        return False

    def set_player_position(self, position):
        self.player_position = position

    def set_monster_position(self, position):
        self.monster_position = position

    def set_entity_position(self, position, value=MapEntity.EMPTY_CELL):
        (row, col) = position
        self.entity_map[row][col] = value

    def get_value_at(self, position):
        (row, col) = position
        return self.entity_map[row][col]

    def print_map(self):
        for row in self.entity_map:
            for cell in row:
                match cell:
                    case MapEntity.EMPTY_CELL:
                        print(' ', end='')
                    case MapEntity.WALL:
                        print(colored('#', 'yellow'), end='')
                    case MapEntity.PLAYER:
                        print(colored('J', 'green'), end='')
                    case MapEntity.MONSTER:
                        print(colored('M', 'red'), end='')
                    case MapEntity.EXIT:
                        print(colored('E', 'blue'), end='')
            print()

    def is_edge_position(self, position):
        (row, col) = position
        return (row == 0 or row == self.map_size[0] - 1) or (col == 0 or col == self.map_size[1] - 1)

    def get_all_positions(self):
        """
        Returns a list of all positions in the map
        :return: list of tuples
        """

        return [(row, col) for row in range(self.map_size[0]) for col in range(self.map_size[1])]

    def get_next_positions(self, current_position):
        """
        Returns a list of all valid positions (in matrix and not walls) that are next to the current position
        :param current_position: tuple
        :return: list of tuples
        """
        (row, col) = current_position
        next_positions = []
        # UP
        if row > 0 and self.entity_map[row - 1][col] != MapEntity.WALL:
            next_positions.append((row - 1, col))
        # DOWN
        if row < self.map_size[0] - 1 and self.entity_map[row + 1][col] != MapEntity.WALL:
            next_positions.append((row + 1, col))
        # LEFT
        if col > 0 and self.entity_map[row][col - 1] != MapEntity.WALL:
            next_positions.append((row, col - 1))
        # RIGHT
        if col < self.map_size[1] - 1 and self.entity_map[row][col + 1] != MapEntity.WALL:
            next_positions.append((row, col + 1))

        return next_positions

    def is_move_possible(self, dx, dy):
        """
        Checks if a move is possible from the current position
        :param dx: int
        :param dy: int
        :return: bool
        """

        (row, col) = self.player_position
        return self.is_in_matrix(row + dx, col + dy) \
            and (
                    self.entity_map[row + dx][col + dy] == MapEntity.EMPTY_CELL
                    or self.entity_map[row + dx][col + dy] == MapEntity.PLAYER
            )

    def is_in_matrix(self, row, col):
        return 0 <= row < self.map_size[0] and 0 <= col < self.map_size[1]