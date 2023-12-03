from collections import namedtuple
from math import prod

from validate import validate


def get_engine_parts(input):
    EnginePart = namedtuple('EnginePart', ['num', 'y', 'x_min', 'x_max'])
    Symbol = namedtuple('Symbol', ['sym', 'y', 'x'])
    engine_parts = []
    symbols = []
    input_lines = open(input).read().split('\n')
    for y in range(len(input_lines)):
        num_buf = ''
        line = input_lines[y]
        for x in range(len(line)):
            sym = line[x]
            if sym.isdigit():
                num_buf += sym
                if x == len(line) - 1:
                    engine_parts.append(EnginePart(int(num_buf), y, x - len(num_buf) + 1, x))
                    num_buf = ''
                continue
            if num_buf != '':
                engine_parts.append(EnginePart(int(num_buf), y, x - len(num_buf), x - 1))
                num_buf = ''
            if sym != ".":
                symbols.append(Symbol(sym, y, x))
    engine_parts = [engine_part for engine_part in engine_parts if is_valid_engine_part(engine_part, symbols)]
    non_engine_parts = [engine_part for engine_part in engine_parts if not is_valid_engine_part(engine_part, symbols)]
    return engine_parts, non_engine_parts, symbols


def is_valid_engine_part(part, symbols):
    for symbol in symbols:
        if in_range(part.y, part.y, symbol.y) and in_range(part.x_min, part.x_max, symbol.x):
            return True
    return False


def in_range(min, max, sym):
    return min - 1 <= sym <= max + 1


def get_engine_parts_sum(input):
    engine_parts, non_engine_parts, symbols = get_engine_parts(input)
    # print_engine_file(engine_parts, non_engine_parts, symbols)
    return sum(engine_part.num for engine_part in engine_parts)


def find_gear_ratios(engine_parts, symbols):
    gears = [sym for sym in symbols if sym.sym == '*']
    part_numbers = [find_gear_parts(gear, engine_parts) for gear in gears]
    return [prod(parts) for parts in part_numbers if len(parts) == 2]


def find_gear_parts(gear, engine_parts):
    return [part.num for part in engine_parts if in_range(part.y, part.y, gear.y) and in_range(part.x_min, part.x_max, gear.x)]


def get_gear_ratios_sum(input):
    engine_parts, non_engine_parts, symbols = get_engine_parts(input)
    return sum(gear_ratio for gear_ratio in find_gear_ratios(engine_parts, symbols))


def print_engine_file(engine_parts, non_engine_parts, symbols):
    max_x = max(max([symbol.x for symbol in symbols]),
                max([engine_part.x_max for engine_part in engine_parts]),
                max([non_engine_part.x_max for non_engine_part in non_engine_parts]))
    max_y = max(max([symbol.y for symbol in symbols]),
                max([engine_part.y for engine_part in engine_parts]),
                max([non_engine_part.y for non_engine_part in non_engine_parts]))
    y = 0
    while y <= max_y:
        x = 0
        while x <= max_x:
            sym = next((sym.sym for sym in symbols if sym.x == x and sym.y == y), None)
            if sym:
                print(sym, end='')
                x += 1
                continue
            part = next((part for part in engine_parts if part.x_min == x and part.y == y), None)
            if part:
                print(part.num, end='')
                x += len(str(part.num))
                continue
            non_part = next((part for part in non_engine_parts if part.x_min == x and part.y == y), None)
            if non_part:
                non_part_Len = len(str(non_part.num))
                for _ in range(non_part_Len):
                    print('X', end='')
                x += non_part_Len
                continue
            print('.', end='')
            x += 1
        print()
        y += 1


validate(get_engine_parts_sum, 'data/day03_example.txt', 4361)
validate(get_engine_parts_sum, 'data/day03_input.txt', 535235)
validate(get_gear_ratios_sum, 'data/day03_example.txt', 467835)
validate(get_gear_ratios_sum, 'data/day03_input.txt', 79844424)
