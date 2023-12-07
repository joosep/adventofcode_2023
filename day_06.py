from collections import namedtuple
from math import prod, sqrt, ceil, floor

from validate import validate

Race = namedtuple("Race", ["time", 'distance'])


def get_races(input):
    data = [[int(x) for x in line[10:].split()] for line in open(input).read().split("\n")]
    return [Race(data[0][i], data[1][i]) for i in range(len(data[0]))]


def get_hold_times(time, distance):
    """
    distance = hold_time*(total_time-hold_time)
    distance=-hold_time**2+total_time*hold_time
    hold_time**2-total_time*hold_time+distance=0
    hold_time=total_time+-sqrt(total_time**2-4*distance)/2
    """
    distance = distance + 1
    return (
        ceil((time - sqrt(time ** 2 - 4 * distance)) / 2),
        floor((time + sqrt(time ** 2 - 4 * distance)) / 2)
    )


def get_ways_to_win(race: Race):
    print(race)
    hold_times = get_hold_times(race.time, race.distance)
    print(hold_times)
    return hold_times[1] - hold_times[0] + 1


def get_possible_wins(input):
    races = get_races(input)
    return prod(get_ways_to_win(race) for race in races)


def get_single_race_win(input):
    races = get_races(input)
    race = Race(
            int(''.join([str(r.time) for r in races])),
            int(''.join([str(r.distance) for r in races])),
    )
    return get_ways_to_win(race)


validate(get_possible_wins, 'data/day06_example.txt', 288)
validate(get_possible_wins, 'data/day06_input.txt', 211904)
validate(get_single_race_win, 'data/day06_example.txt', 71503)
validate(get_single_race_win, 'data/day06_input.txt', 43364472)
