import os
import random
from lib.map.map import Map
from lib.map.map_entity import MapEntity


def mark_random_player_position(game_map):
    """
    Marks a random player position in the map by choosing a random position from the valid positions
    :param game_map:
    """
    player_position = random.choice(game_map.get_player_valid_positions())
    game_map.set_player_position(player_position)
    game_map.set_entity_position(player_position, value=MapEntity.PLAYER)


def mark_random_monster_position(game_map):
    """
    Marks a random monster position in the map by choosing a random position from the valid positions
    :param game_map:
    """
    monster_position = random.choice(game_map.get_monster_valid_positions())
    game_map.set_monster_position(monster_position)
    game_map.set_entity_position(monster_position, value=MapEntity.MONSTER)


def get_random_map():
    """
    Generates a random map using the assets folder and mark a random player and monster position
    :return: Map object
    """

    # get current project folder
    project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # remove the last folder from the path
    project_folder = os.path.dirname(project_folder)

    base_path = f'{project_folder}/assets/maps/map'
    base_extension = '.txt'
    map_number = random.randint(1, 5)

    map_path = base_path + str(map_number) + base_extension
    game_map = Map(map_path)

    mark_random_player_position(game_map)
    mark_random_monster_position(game_map)

    return game_map
