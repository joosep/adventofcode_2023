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
        mappings_list.append(sorted(mappings, key=lambda x: x.src))
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


def find_location_number_in_range(seed_ranges, mappings_list):
    for mappings in mappings_list:
        seed_ranges = merge_seeds(seed_ranges)
        remapped_seeds = []
        for seed_start, seed_end in seed_ranges:
            for mapping in mappings:
                seed_before_mapping_start = seed_start if seed_start < mapping.src else None
                seed_before_mapping_end = min(seed_start, mapping.src - 1) if seed_before_mapping_start else None
                seed_mapping_start = max(seed_start, mapping.src) \
                    if mapping.src <= seed_end and seed_start <= mapping.src_max else None
                seed_mapping_end = min(mapping.src_max, seed_end) if seed_mapping_start else None
                seed_after_mapping_start = mapping.src_max + 1 if mapping.src_max < seed_end else None
                seed_after_mapping_end = seed_end if seed_after_mapping_start else None
                # print(f'seeds before: {seed_before_mapping_start} - {seed_before_mapping_end}, '
                #      f'seed mapping start: {seed_mapping_start} - {seed_mapping_end}, '
                #      f'seeds after: {seed_after_mapping_start} - {seed_after_mapping_end}')
                if seed_before_mapping_start:
                    remapped_seeds.append((seed_start, seed_before_mapping_end))  # start to src or end
                if seed_mapping_start:
                    remapped_seeds.extend(get_new_seed_range(seed_start, seed_mapping_end, mapping))
                if seed_after_mapping_start:
                    seed_start = max(seed_start, seed_after_mapping_start)
                    continue
                else:
                    break
            if seed_after_mapping_start:
                remapped_seeds.append((seed_start + 1, seed_end))
        seed_ranges = merge_seeds(remapped_seeds)
        print(f'next seeds: {seed_ranges}')
        print('----')
    return min(seed[0] for seed in seed_ranges)


def get_min_loc_number(input):
    seeds, mappings_list = convert_input(input)
    return min(find_location_number(seed, mappings_list) for seed in seeds)


def get_min_loc_number_in_range(input):
    seeds, mappings_list = convert_input(input)
    seed_ranges = [(int(seed[0]), int(seed[0]) + int(seed[1])) for seed in list(zip(seeds[::2], seeds[1::2]))]
    return find_location_number_in_range(seed_ranges, mappings_list)


validate(get_min_loc_number, 'data/day05_example.txt', 35)
validate(get_min_loc_number, 'data/day05_input.txt', 177942185)
validate(get_min_loc_number_in_range, 'data/day05_example.txt', 46)
validate(get_min_loc_number_in_range, 'data/day05_input.txt', 69841803)
