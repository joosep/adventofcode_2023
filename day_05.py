from collections import namedtuple

from validate import validate

Mapping = namedtuple('Mapping', ['dest', 'src', 'src_max'])


def convert_input(input):
    sets = open(input).read().split('\n\n')
    seeds = sets.pop(0).split(":")[1].strip().split(" ")
    mappings_list = []
    for set in sets:
        lines = set.split('\n')
        lines.pop(0)
        mappings = []
        for line in lines:
            dest, src, range_length = line.split(' ')
            mappings.append(Mapping(int(dest), int(src), int(src) + int(range_length) - 1))
        mappings_list.append(mappings)
    return seeds, mappings_list


def map_value(value: int, mapping: Mapping):
    if mapping.src <= value <= mapping.src_max:
        return mapping.dest - mapping.src + value
    return None


def find_location_number(seed, mappings_list):
    new_seed = int(seed)
    for mappings in mappings_list:
        for mapping in mappings:
            new_value = map_value(new_seed, mapping)
            if new_value:
                new_seed = new_value
                break
    return new_seed


def keep_unused(start, end, used_start, used_end):
    start_ends = []
    if start < used_start:
        start_ends.append((start, min(end, used_start - 1)))
    if end > used_end:
        start_ends.append((max(start, used_end + 1), end))
    return start_ends


def find_one_to_one_mappings(seed_ranges, remap_ranges):
    ranges_to_check = seed_ranges
    for used_start, used_end in remap_ranges:
        new_seed_ranges = []
        for seed_start, seed_end in ranges_to_check:
            new_seed_ranges.extend(keep_unused(seed_start, seed_end, used_start, used_end))
        ranges_to_check = new_seed_ranges
    return ranges_to_check


def merge_seeds(ranges):
    ranges.sort(key=lambda x: x[0])
    new_ranges = []
    for start, end in ranges:
        if not new_ranges:
            new_ranges.append((start, end))
            continue
        last_end = new_ranges[-1][1]
        last_start = new_ranges[-1][0]
        if last_end + 1 >= start:
            new_ranges[-1] = (last_start, max(last_end, end))
        else:
            new_ranges.append((start, end))
    return new_ranges


def find_location_number_in_range(seed_ranges, mappings_list):
    for mappings in mappings_list:
        print(f'seeds: {seed_ranges}')
        remap_ranges = merge_seeds([(mapping.src, mapping.src_max) for mapping in mappings])
        print(f'remap_ranges: {sorted(remap_ranges, key=lambda x: x[0])}')
        for src_start, src_end in merge_seeds(find_one_to_one_mappings(seed_ranges, remap_ranges)):
            mappings.append(Mapping(src_start, src_start, src_end))
        print(f'mappings: {mappings}')
        remapped_seeds = []
        for seed_start, seed_end in seed_ranges:
            for mapping in mappings:
                remapped_seeds.extend(get_new_seed_range(seed_start, seed_end, mapping))
        print(f'remapped_seeds: {sorted(remapped_seeds, key=lambda x: x[0])}')
        seed_ranges = merge_seeds(remapped_seeds)
        print(f'final_list: {seed_ranges}')
        print('----')
    return min(seed[0] for seed in seed_ranges)


def get_new_seed_range(seed_start, seed_end, mapping):
    if (mapping.src <= seed_start <= mapping.src_max) or \
            (mapping.src <= seed_end <= mapping.src_max):
        # src is in the seed range
        min_end_seed = min(seed_end, mapping.src_max)
        max_start_seed = max(seed_start, mapping.src)
        seed_dest_start = mapping.dest - mapping.src + max_start_seed
        seed_dest_end = mapping.dest - mapping.src + min_end_seed
        return [(seed_dest_start, seed_dest_end)]
    return []


def get_min_loc_number(input):
    seeds, mappings_list = convert_input(input)
    return min(find_location_number(seed, mappings_list) for seed in seeds)


def get_min_loc_number_in_range(input):
    seeds, mappings_list = convert_input(input)
    seed_ranges = [(int(seed[0]), int(seed[0]) + int(seed[1])) for seed in list(zip(seeds[::2], seeds[1::2]))]
    return find_location_number_in_range(merge_seeds(seed_ranges), mappings_list)


validate(get_min_loc_number, 'data/day05_example.txt', 35)
validate(get_min_loc_number, 'data/day05_input.txt', 177942185)
validate(get_min_loc_number_in_range, 'data/day05_example.txt', 46)
# validate(get_min_loc_number_in_range, 'data/day05_input.txt')  # answer is between 52360685 - 85624563
