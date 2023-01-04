import random
from lib.map.map import Map
from lib.map.map_entity import MapEntity


def mark_random_player_position(game_map):
    player_position = random.choice(game_map.get_player_valid_positions())
    game_map.set_player_position(player_position)
    game_map.set_entity_position(player_position, value=MapEntity.PLAYER)


def mark_random_monster_position(game_map):
    monster_position = random.choice(game_map.get_monster_valid_positions())
    game_map.set_monster_position(monster_position)
    game_map.set_entity_position(monster_position, value=MapEntity.MONSTER)


def get_random_map():
    base_path = '../../maps/map'
    base_extension = '.txt'
    map_number = random.randint(1, 5)

    map_path = base_path + str(map_number) + base_extension
    print(f'Using map: {map_path}')
    game_map = Map(map_path)

    mark_random_player_position(game_map)
    mark_random_monster_position(game_map)

    return game_map


new_map = get_random_map()
new_map.print_map()