from math import prod

from validate import validate


def parse_pick(pick):
    split = pick.strip().split(' ')
    return {split[1]: split[0]}


def parse_game(line):
    id_line, picks_line = line.split(':')
    game_id = int(id_line.split(' ')[1])
    picks_list = [[parse_pick(pick) for pick in picks.strip().split(',')] for picks in picks_line.split(';')]
    pick_set = {}
    for pick in [pick for pick_list in picks_list for pick in pick_list]:
        for color, count in pick.items():
            old_count = pick_set.get(color, 0)
            pick_set[color] = int(count) if old_count < int(count) else old_count
    return {'id': game_id, 'picks': pick_set}


def is_valid(game, valid_game):
    for color in game['picks']:
        count = game['picks'][color]
        if color not in valid_game:
            return False
        if valid_game[color] < count:
            return False
    return True


def get_valid_games_sum(input, valid_game={'red': 12, 'green': 13, 'blue': 14}):
    return sum(game['id'] for game in [parse_game(line) for line in open(input).read().split('\n')] if is_valid(game, valid_game))


def get_power_of_min_cubes(input):
    return sum(prod([game['picks'][color] for color in game['picks']]) for game in
               [parse_game(line) for line in open(input).read().split('\n')])


validate(get_valid_games_sum, 'data/day02_example.txt', 8)
validate(get_valid_games_sum, 'data/day02_input.txt', 2600)
validate(get_power_of_min_cubes, 'data/day02_example.txt', 2286)
validate(get_power_of_min_cubes, 'data/day02_input.txt', 86036)
