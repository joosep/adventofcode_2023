from validate import validate


def get_history(line):
    history_row = [int(x) for x in line.split()]
    history_rows = [history_row]
    while True:
        new_history_row = []
        for i in range(len(history_rows[-1]) - 1):
            new_history_row.append(history_rows[-1][i + 1] - history_rows[-1][i])
        history_rows.append(new_history_row)
        if sum(new_history_row) == 0:
            break
    return history_rows


def get_history_value(line):
    return sum(row[-1] for row in get_history(line))


def get_history_sum(input):
    return sum(get_history_value(line) for line in open(input).read().split('\n') if line != '')


def get_backward_value(history_rows):
    cur_value = 0
    for value in [row[0] for row in reversed(history_rows)]:
        cur_value = value - cur_value
    return cur_value


def get_history_backwards_sum(input):
    return sum(get_backward_value(get_history(line)) for line in open(input).read().split('\n') if line != '')


validate(get_history_sum, 'data/day09_example.txt', 114)
validate(get_history_sum, 'data/day09_input.txt', 1806615041)
validate(get_history_backwards_sum, 'data/day09_example.txt', 2)
validate(get_history_backwards_sum, 'data/day09_input.txt', 1211)
