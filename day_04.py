from validate import validate


def find_winnings(line):
    card, winnings_and_num_parts = line.split(":")
    winning_parts, num_parts = winnings_and_num_parts.split("|")
    winning_nums = set(num.strip() for num in winning_parts.split(" ") if num != '')
    numbers = set(num.strip() for num in num_parts.split(" ") if num != '')
    return len(winning_nums & numbers)


def calc_points(line):
    winnings = find_winnings(line)
    return 2 ** (winnings - 1) if winnings > 0 else 0


def get_points_sum(input):
    return sum(calc_points(line) for line in open(input).read().split('\n'))


def calc_cards(line, copies_stack):
    winnings = find_winnings(line)
    card_copies = update_copies(copies_stack, winnings)
    return card_copies


def update_copies(copies_stack, winnings):
    card_copies = 1 + (copies_stack.pop(0) if copies_stack else 0)
    for i in range(winnings):
        if len(copies_stack) > i:
            copies_stack[i] += card_copies
        else:
            copies_stack.append(card_copies)
    return card_copies


def get_cards_sum(input):
    copies_stack = []
    return sum(calc_cards(line, copies_stack) for line in open(input).read().split('\n'))


validate(get_points_sum, 'data/day04_example.txt', 13)
validate(get_points_sum, 'data/day04_input.txt', 25010)
validate(get_cards_sum, 'data/day04_example.txt', 30)
validate(get_cards_sum, 'data/day04_input.txt', 9924412)
