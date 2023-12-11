from validate import validate


def get_empty_rows_cols(input):
    universe = [line for line in open(input).read().split('\n') if line != '']
    rows = [r for r in range(len(universe)) if all(c != "#" for c in universe[r])]
    cols = [c for c in range(len(universe[0])) if all(r[c] != "#" for r in universe)]
    return rows, cols


def get_galaxies_coords(input, rows, cols, expanse=1):
    universe = [line for line in open(input).read().split('\n') if line != '']
    coords = [(r, c) for r in range(len(universe)) for c in range(len(universe[0])) if universe[r][c] == "#"]
    galaxies = []
    for (r, c) in coords:
        r += sum(expanse for i in rows if i < r)
        c += sum(expanse for i in cols if i < c)
        galaxies.append((r, c))
    return galaxies


def get_distance_sum(galaxies):
    sum = 0
    for i in range(len(galaxies)):
        for j in range(i + 1, len(galaxies)):
            distance = abs(galaxies[i][0] - galaxies[j][0]) + abs(galaxies[i][1] - galaxies[j][1])
            sum += distance
    return sum


def get_shortest_paths_sum(input):
    rows, cols = get_empty_rows_cols(input)
    galaxies = get_galaxies_coords(input, rows, cols)
    return get_distance_sum(galaxies)


def get_shortest_paths_sum2(input):
    rows, cols = get_empty_rows_cols(input)
    galaxies = get_galaxies_coords(input, rows, cols, 1000000 - 1)
    return get_distance_sum(galaxies)


validate(get_shortest_paths_sum, 'data/day11_example.txt', 374)
validate(get_shortest_paths_sum, 'data/day11_input.txt', 9370588)
validate(get_shortest_paths_sum2, 'data/day11_input.txt', 746207878188)
