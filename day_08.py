from collections import namedtuple

from validate import validate


def parse_nodes(input):
    instructions, node_lines = open(input).read().split('\n\n')
    nodes = {}
    [nodes.update({node[:3]: {"L": node[7:10], "R": node[12:15]}}) for node in node_lines.split('\n')]
    return instructions, nodes


def count_steps(cur_node, instructions, nodes):
    steps = 0
    while True:
        for instruction in instructions:
            if cur_node == 'ZZZ':
                return steps
            cur_node = nodes[cur_node][instruction]
            steps += 1


instr = namedtuple('instr', ['n', 'i', 'l'])
z_value_cycle = namedtuple('z_value_cycle', ['cur_z_value', 'cur_z_values_ndx', 'cycle_count', 'z_values', 'length'])


def find_Z_cycles(cur_node, instructions, nodes):
    steps = 0
    seen_cur_node_and_instruction = []
    z_locations = []
    while True:
        for i in range(len(instructions)):
            instruction = instructions[i]
            if cur_node[2] == 'Z':
                z_locations.append(steps)
            cur_instr = instr(cur_node, instruction, i)
            if cur_instr in seen_cur_node_and_instruction:
                cycle_start = seen_cur_node_and_instruction.index(cur_instr)
                return z_value_cycle(z_locations[0], 0, 0, z_locations, steps - cycle_start)
            seen_cur_node_and_instruction.append(cur_instr)
            cur_node = nodes[cur_node][instruction]
            steps += 1


def update_cur_z_value(c, cur_z_value):
    if cur_z_value <= c.cur_z_value:
        return c
    new_value = c.cur_z_value
    new_cycle_count = c.cycle_count
    new_ndx = c.cur_z_values_ndx
    while cur_z_value > new_value:
        if new_ndx == (len(c.z_values) - 1):
            new_cycle_count += 1
            new_ndx = 0
            new_value = c.z_values[new_ndx] + new_cycle_count * c.length
        else:
            new_ndx += 1
            new_value = c.z_values[new_ndx] + new_cycle_count * c.length
    return c._replace(cur_z_value=new_value, cur_z_values_ndx=new_ndx, cycle_count=new_cycle_count)


def count_ghosts_steps(cur_nodes, instructions, nodes):
    z_cycles = [find_Z_cycles(cur_node, instructions, nodes) for cur_node in cur_nodes]
    [print(z_cycle) for z_cycle in z_cycles]
    cur_z_value = max(z_cycle.cur_z_value for z_cycle in z_cycles)
    while True:
        if all(cur_z_value == z_cycle.cur_z_value for z_cycle in z_cycles):
            return cur_z_value
        z_cycles = [update_cur_z_value(z_cycle, cur_z_value) for z_cycle in z_cycles]
        cur_z_value = max(z_cycle.cur_z_value for z_cycle in z_cycles)


# length*(z_value-start)+start
def get_steps_to_ZZZ(input):
    return count_steps('AAA', *parse_nodes(input))


def get_ghost_steps_Z(input):
    instructions, nodes = parse_nodes(input)
    return count_ghosts_steps({node for node in nodes if node[2] == "A"}, instructions, nodes)


validate(get_steps_to_ZZZ, 'data/day08_example.txt', 2)
validate(get_steps_to_ZZZ, 'data/day08_input.txt', 14893)
validate(get_ghost_steps_Z, 'data/day08_example2.txt', 6)
validate(get_ghost_steps_Z, 'data/day08_input.txt')
