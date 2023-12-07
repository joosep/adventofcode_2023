from collections import namedtuple
from itertools import groupby

from validate import validate

Hand = namedtuple('Hand', ['hand', 'bid', 'type', 'groups'])


def parse_cards(cards):
    def parse_card(card):
        if card == 'A':
            return 14
        if card == 'K':
            return 13
        if card == 'Q':
            return 12
        if card == 'J':
            return 11
        if card == 'T':
            return 10
        return int(card)

    return [parse_card(card) for card in cards]


types = {'five of kind': 6, 'four of kind': 5, 'full house': 4, 'three of kind': 3,
         'two pair': 2, 'one pair': 1, 'high card': 0}


def get_hand_type(hand):
    hand = [(len(list(group)), key) for key, group in groupby(sorted(hand))]
    grouped_hand = sorted(hand, reverse=True)
    if grouped_hand[0][0] == 5:
        return types['five of kind'], grouped_hand
    if grouped_hand[0][0] == 4:
        return types['four of kind'], grouped_hand
    if grouped_hand[0][0] == 3:
        if grouped_hand[1][0] == 2:
            return types['full house'], grouped_hand
        return types['three of kind'], grouped_hand
    if grouped_hand[0][0] == 2:
        if grouped_hand[1][0] == 2:
            return types['two pair'], grouped_hand
        return types['one pair'], grouped_hand
    return types['high card'], grouped_hand


def parse_hands(input):
    hands = []
    for line in open(input).read().split('\n'):
        cards, bid = line.split(" ")
        hand = parse_cards(cards)
        hands.append(Hand(hand, int(bid), *get_hand_type(hand)))
    return hands


def get_total_winnings(input):
    hands = parse_hands(input)
    hands = sorted(hands, key=lambda x: [x.type, *x.hand], reverse=True)
    sum = 0
    for i in range(1, len(hands) + 1):
        hand = hands[len(hands) - i]
        sum += hand.bid * i
    return sum


def replace_joker(hand):
    grouped_hands_seen = []  # 3J, 1A,1A
    new_type = hand.type
    for count, card in hand.groups:
        if card == 11:
            if grouped_hands_seen:
                first_group = grouped_hands_seen[0]
                if first_group == 4:
                    new_type = types['five of kind']
                elif first_group == 3:
                    if count == 2:
                        new_type = types['five of kind']
                    else:
                        new_type = types['four of kind']
                elif first_group == 2:
                    if sum(1 for group in grouped_hands_seen if group == 2) == 2:
                        new_type = types['full house']
                    elif count == 3:
                        new_type = types['five of kind']
                    elif count == 2:
                        new_type = types['four of kind']
                    else:
                        new_type = types['three of kind']
                else:
                    new_type = types['one pair']
            else:
                if count == 5:
                    break
                elif count == 4:
                    new_type = types['five of kind']
                elif count == 3:
                    if hand.groups[1][0] == 2:
                        new_type = types['five of kind']
                    else:
                        new_type = types['four of kind']
                elif count == 2:
                    if hand.groups[1][0] == 2:
                        new_type = types['four of kind']
                    else:
                        new_type = types['three of kind']
                else:
                    new_type = types['one pair']
            break
        grouped_hands_seen.append(count)
    return Hand([num if num != 11 else -1 for num in hand.hand], hand.bid, new_type, hand.groups)


def get_w_joker_total_winnings(input):
    hands = [replace_joker(hand) for hand in parse_hands(input)]

    hands = sorted(hands, key=lambda x: [x.type, *x.hand], reverse=True)
    sum = 0
    for i in range(1, len(hands) + 1):
        hand = hands[len(hands) - i]
        print(hand, i)
        sum += hand.bid * i
    return sum


validate(get_total_winnings, 'data/day07_example.txt', 6440)
validate(get_total_winnings, 'data/day07_input.txt', 253910319)
validate(get_w_joker_total_winnings, 'data/day07_example.txt', 5905)
validate(get_w_joker_total_winnings, 'data/day07_input.txt', 254083736)
