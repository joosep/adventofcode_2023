from validate import validate

cache_map = {}


def find_arrangement_cache(springs, groups):
    key = str((springs, groups))
    if key in cache_map:
        return cache_map[key]
    arrangements = find_arrangement(springs, groups)
    cache_map[key] = arrangements
    return arrangements


def has_spring(springs):
    return any(spring == "#" for spring in springs)


def find_arrangement(springs_groups, group_counts):
    if len(springs_groups) > 0 and springs_groups[0] == '':
        springs_groups.pop(0)
    if len(group_counts) == 0:
        has_not_springs = not any(has_spring(springs) for springs in springs_groups)
        return int(has_not_springs)
    if len(springs_groups) == 0:
        return 0

    cur_group = springs_groups[0]
    cur_group_count = group_counts[0]
    cur_match = cur_group[:cur_group_count]
    if len(cur_group) < cur_group_count:
        if has_spring(cur_match):
            return 0
        return find_arrangement_cache(springs_groups[1:], group_counts.copy())
    final_arrangements = 0
    if len(cur_group) > cur_group_count and cur_group[cur_group_count] == "?":
        final_arrangements = find_arrangement_cache([cur_group[cur_group_count + 1:]] + springs_groups[1:], group_counts[1:])
    if len(cur_group) == cur_group_count:
        final_arrangements += find_arrangement_cache(springs_groups[1:], group_counts[1:])
    if len(cur_group) >= cur_group_count:
        if cur_group[0] != "#":
            final_arrangements += find_arrangement_cache([cur_group[1:]] + springs_groups[1:], group_counts.copy())
    return final_arrangements


def get_arrangements(line):
    print(f'===================================')
    print(f'input: {line}')
    springs_groups = [spring for spring in line.split(' ')[0].split('.') if spring != '']
    group_counts = [int(count) for count in line.split(' ')[1].split(',')]
    arrangements = find_arrangement(springs_groups, group_counts)
    print(f'arrangements: {arrangements}')
    return arrangements


def get_arrangement_sum(input):
    return sum(get_arrangements(line) for line in open(input).read().split('\n') if line != '')


def unfold_record(line):
    springs = line.split(' ')[0]
    groups = line.split(' ')[1]
    return f'{springs}?{springs}?{springs}?{springs}?{springs} {groups},{groups},{groups},{groups},{groups}'


def get_exploded_arrangement_sum(input):
    return sum(get_arrangements(unfold_record(line)) for line in open(input).read().split('\n') if line != '')


assert get_arrangements('.. 1') == 0
assert get_arrangements('?? 1') == 2
assert get_arrangements('??? 1') == 3
assert get_arrangements('?.? 1') == 2
assert get_arrangements('?.# 1') == 1
assert get_arrangements('?.# 1,1') == 1
assert get_arrangements('??#.?? 2,1') == 2

validate(get_arrangement_sum, 'data/day12_example.txt', 21)
validate(get_arrangement_sum, 'data/day12_input.txt', 7407)
validate(get_exploded_arrangement_sum, 'data/day12_example.txt', 525152)
validate(get_exploded_arrangement_sum, 'data/day12_input.txt', 30568243604962)
