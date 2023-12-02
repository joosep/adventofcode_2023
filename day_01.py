from validate import validate


def keep_digits(line):
    return [d for d in line if d.isdigit()]


def sum_digits(input):
    return sum(int(f'{digits[0]}{digits[-1]}') for digits in [keep_digits(line) for line in open(input).read().split('\n')])


digit_words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def get_first_last_digits(line):
    digits = []
    for i in range(len(line)):
        if line[i].isdigit():
            digits.append(line[i])
            continue
        for word in digit_words:
            if line[i:].startswith(word):
                digits.append(digit_words.index(word))
                i += len(word)
                continue
    return f'{digits[0]}{digits[-1]}'


def sum_word_digits(input):
    return sum(int(get_first_last_digits(line)) for line in open(input).read().split('\n'))


validate(sum_digits, 'data/day01_example.txt', 142)
validate(sum_digits, 'data/day01_input.txt', 53080)
validate(sum_word_digits, 'data/day01_example2.txt', 281)
validate(sum_word_digits, 'data/day01_input.txt', 53268)
