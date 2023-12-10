from validate import validate


def get_farthest_length(input):
    s_loc, tiles = parse_tiles(input)
    length = 0
    last_loc1, last_loc2 = None, None
    cur_loc1, cur_loc2 = tiles[s_loc]
    while True:
        if last_loc1 is None:
            last_loc1, last_loc2 = s_loc, s_loc
            cur_loc1, cur_loc2 = tiles[s_loc]
        else:
            cur_loc1, last_loc1 = next(loc for loc in tiles[cur_loc1] if loc != last_loc1), cur_loc1
            cur_loc2, last_loc2 = next(loc for loc in tiles[cur_loc2] if loc != last_loc2), cur_loc2
        length += 1
        if cur_loc1 == cur_loc2:
            return length


def parse_tiles(input):
    grid = [line for line in open(input).read().split('\n') if line != '']
    tiles = {}
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            loc = (x, y)
            sym = grid[y][x]
            if sym == 'S':
                s_loc = (x, y)
                continue
            tile = get_tile_coords(sym, x, y)
            tiles[loc] = tile
    s_loc_coords = []
    for (x, y) in [(s_loc[0] - 1, s_loc[1]), (s_loc[0] + 1, s_loc[1]), (s_loc[0], s_loc[1] - 1), (s_loc[0], s_loc[1] + 1)]:
        if x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid):
            if s_loc in tiles[(x, y)]:
                s_loc_coords.append((x, y))
    tiles[s_loc] = s_loc_coords
    return s_loc, tiles


def get_tile_coords(sym, x, y):
    if sym == '|':
        tile = [(x, y + 1), (x, y - 1)]
    elif sym == '-':
        tile = [(x + 1, y), (x - 1, y)]
    elif sym == "L":
        tile = [(x + 1, y), (x, y - 1)]
    elif sym == "J":
        tile = [(x, y - 1), (x - 1, y)]
    elif sym == "7":
        tile = [(x, y + 1), (x - 1, y)]
    elif sym == "F":
        tile = [(x + 1, y), (x, y + 1)]
    else:
        tile = []
    return tile


def get_tiles_within_loop(input):
    s_loc, tiles = parse_tiles(input)
    loop_locs = get_loop_locs(s_loc, tiles)
    max_x = max(loc[0] for loc in tiles)
    max_y = max(loc[1] for loc in tiles)
    within_loop_count = 0
    for y in range(max_y + 1):
        in_loop = False
        pipe_started_direction = None
        for x in range(max_x + 1):
            cur_loc = (x, y)
            if cur_loc in loop_locs:
                direction = get_tile_direction(cur_loc, tiles[cur_loc])
                if pipe_started_direction == None:
                    if direction == 'vertical':
                        in_loop = not in_loop
                    else:
                        pipe_started_direction = direction
                else:
                    if direction != 'horizontal':
                        if direction != pipe_started_direction:
                            in_loop = not in_loop
                        pipe_started_direction = None
                print(direction[0], end='')
                continue
            elif in_loop:
                within_loop_count += 1
            print('I' if in_loop else 'O', end='')
        print()
    return within_loop_count


def get_loop_locs(s_loc, tiles):
    loop_locs = set()
    last_loc = s_loc
    loop_locs.add(s_loc)
    cur_loc, _ = tiles[s_loc]
    while True:
        loop_locs.add(cur_loc)
        cur_loc, last_loc = next(loc for loc in tiles[cur_loc] if loc != last_loc), cur_loc
        if cur_loc == s_loc:
            return loop_locs


def get_tile_direction(cur_loc, tile):
    y_dist = abs(tile[0][1] - tile[1][1])
    if y_dist == 2:
        return 'vertical'
    if y_dist == 0:
        return 'horizontal'
    max_y = max(tile[0][1], tile[1][1])
    if cur_loc[1] < max_y:
        return "down"
    else:
        return "up"


validate(get_farthest_length, 'data/day10_example.txt', 4)
validate(get_farthest_length, 'data/day10_example2.txt', 8)
validate(get_farthest_length, 'data/day10_input.txt', 6800)
validate(get_tiles_within_loop, 'data/day10_example3.txt', 4)
validate(get_tiles_within_loop, 'data/day10_example4.txt', 10)
validate(get_tiles_within_loop, 'data/day10_input.txt',483)
