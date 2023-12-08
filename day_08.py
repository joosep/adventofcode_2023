from validate import validate


def parse_nodes(input):
    hands = []
    instructions, node_lines = open(input).read().split('\n\n')
    nodes = {}
    [nodes.update({node[:3]: {"L": node[7:10], "R": node[12:15]}}) for node in node_lines.split('\n')]
    return instructions, nodes


def count_steps(cur_node, instructions, nodes):
    steps = 0
    if cur_node == 'ZZZ':
        return steps
    for instruction in instructions:
        cur_node = nodes[cur_node][instruction]
        steps += 1
    return steps + count_steps(cur_node, instructions, nodes)


def get_steps_to_ZZZ(input):
    return count_steps('AAA', *parse_nodes(input))

#def gt_steps_to_ghost_Z(input):
#    instructions,nodes =parse_nodes(input)
#    return count_steps(set([node if node[2]=="A" for node in nodes), *)

validate(get_steps_to_ZZZ, 'data/day08_example.txt', 2)
validate(get_steps_to_ZZZ, 'data/day08_input.txt', 14893)
#validate(get_steps_to_ghost_Z, 'data/day08_example2.txt',6)
# validate(get_steps_to_ghost_Z, 'data/day08_input.txt')
