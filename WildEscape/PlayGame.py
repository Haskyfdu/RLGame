import random
from typing import List
from copy import deepcopy
from collections import defaultdict


Suit_List = ['Spade', 'Heart', 'Diamond', 'Club']
Suit_Abbreviation = {'S': 'Spade', 'H': 'Heart', 'D': 'Diamond', 'C': 'Club'}
Suit_Dict = {'Spade': '♠', 'Heart': '♥', 'Diamond': '♦', 'Club': '♣',
             'RedJoker': 'RJ', 'BlackJoker': 'BJ'}
Number = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '', '']


class Card:
    def __init__(self, suit, num):
        self.suit = suit
        self.num = num
        assert suit in Suit_Dict, 'Illegal Suit!'
        assert num in list(range(2, 17)), 'Illegal Number!'
        if num == 2:
            self.value = 15  
        elif num >= 15:
            self.value = num + 1
        else:
            self.value = num 

    def __eq__(self, other):
        return self.suit == other.suit and self.num == other.num

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f"{Suit_Dict[self.suit]}{Number[self.num-2]}"


class Deck:
    def __init__(self, n=1):
        self.cards_list = [Card(suit, num) for num in range(2, 15) for suit in Suit_List for _ in range(n)]
        self.cards_list.extend([Card('RedJoker', 16) for _ in range(n)])
        self.cards_list.extend([Card('BlackJoker', 15) for _ in range(n)])

    def shuffle(self):
        random.shuffle(self.cards_list)


class Player:
    def __init__(self, position=0):
        self.position = position
        self.hands = []
        self.played_cards = []
        self.plans = {}

    def set_hands(self, hands: List[Card]):
        self.hands = hands
        self.hands.sort()

    def show_hands(self):
        print(self.hands)


class WildEscapePolicy:
    def __init__(self, cards_list=None):
        self.cards_list = cards_list
        self.plan_list = []

    def identify_cards_from_string(self, input_str: str):
        cards_list = []
        input_str = input_str.upper()
        cards_list.extend([Card('RedJoker', 16) for _ in range(input_str.count('RJ'))])
        cards_list.extend([Card('BlackJoker', 15) for _ in range(input_str.count('BJ'))])
        input_str = input_str.replace('RJ', '')
        input_str = input_str.replace('BJ', '')
        input_str = input_str.replace('10', 'T')
        input_str = input_str.replace('1', 'A')
        suit, n = None, None
        for p in input_str:
            if p in 'SHDC':
                suit = Suit_Abbreviation[p]
            else:
                if p in 'TJQKA':
                    n = 'TJQKA'.index(p) + 10
                else:
                    n = int(p)
                try:
                    cards_list.append(Card(suit, n))
                except:
                    raise ValueError(f'Identification Card Failed: {suit, n}')
        cards_list.sort()
        print(f'Identifying result is {len(cards_list)} cards:')
        print(cards_list)
        self.cards_list = cards_list

    def cards_suit_dict(self, cards_list=None):
        cards_list = self.cards_list if cards_list is None else cards_list
        suit_dict = defaultdict(list)
        for card in cards_list:
            suit_dict[card.suit].append(card)
        return suit_dict

    def cards_num_dict(self, cards_list=None):
        cards_list = self.cards_list if cards_list is None else cards_list
        num_dict = defaultdict(list)
        for card in cards_list:
            num_dict[str(card.num)].append(card)
        return num_dict

    @staticmethod
    def update_plan_else(plan, cards_list):
        for card in cards_list:
            plan['else'].pop(plan['else'].index(card))
        return plan

    def identify_straight(self, cards_list, max_using_joker):
        num_dict = self.cards_num_dict(cards_list)
        num_dict['1'] = num_dict['14']
        num_dict['label'] = [1 if len(num_dict[str(i)]) > 0 else 0 for i in range(1, 15)]
        num_dict['straight_label'] = [sum(num_dict['label'][i: i + 5]) for i in range(10)]
        joker_list = num_dict['15'] + num_dict['16']
        use_joker_num = min(max_using_joker, len(joker_list))
        n = max(num_dict['straight_label'])
        straight_plans_list = [[]]
        if n + use_joker_num < 5:
            return straight_plans_list
        for i, m in enumerate(num_dict['straight_label']):
            if m == n:
                if len(num_dict[str(i + 5)]) == 0:
                    continue
                straight, copy_joker = [], joker_list.copy()
                for j in range(5):
                    if len(num_dict[str(i + j + 1)]) > 0:
                        straight.append(num_dict[str(i + j + 1)][0])
                    else:
                        straight.append(copy_joker.pop(0))
                straight_plans_list.append(straight)
        return straight_plans_list

    def identify_straight_flush(self, cards_list, max_using_joker):
        suit_dict = self.cards_suit_dict(cards_list)
        straight_flush_plans_list = [[]]
        for suit in Suit_List:
            straight_flush_plans_list.extend(self.identify_straight(suit_dict[suit], max_using_joker)[1:])
        return straight_flush_plans_list

    def identify_flush(self, cards_list, max_using_joker):
        suit_dict = self.cards_suit_dict(cards_list)
        num_dict = self.cards_num_dict(cards_list)
        flush_plans_list = [[]]
        for suit in Suit_List:
            n = len(suit_dict[suit])
            if n == 5:
                flush_plans_list.append(suit_dict[suit])
            elif n >= 6:
                flush_label = defaultdict(list)
                for i in range(3, 16):
                    k1 = len([p for p in suit_dict[suit] if p.value == i])
                    if k1 > 0:
                        k2 = len([num_dict[str(i)]])
                        num_type_1 = f"{k2 - k1}"
                        num_type_2 = f"{k2 - k1}-{k2}"
                        flush_label[num_type_1].append(i)
                        flush_label[num_type_2].append(i)
                left = n - 5
                if left == 1:
                    for num_type in ['1', '2', '0']:
                        # todo: 1-2和2-3可以比点数
                        if len(flush_label[num_type]) >= 1:
                            k = flush_label[num_type].pop(-1)
                            k = 2 if k == 15 else k
                            suit_dict[suit].pop(suit_dict[suit].index(Card(suit, k)))
                            flush_plans_list.append(suit_dict[suit])
                            break
                elif left >= 2:
                    m = len(flush_label['1-1']) + 2 * len(flush_label['1-2'])
                    if m < left:
                        # todo
                        flush_plans_list.append(suit_dict[suit][:5])
                    else:
                        a = flush_label['1-1'] + flush_label['1-2']
                        a.sort()
                        b = flush_label['1-2']
                        while left > 0:
                            if len(a) > 0:
                                k = a.pop(-1)
                            else:
                                k = b.pop(-1)
                            k = 2 if k == 15 else k
                            suit_dict[suit].pop(suit_dict[suit].index(Card(suit, k)))
                            left -= 1
                        flush_plans_list.append(suit_dict[suit])
        return flush_plans_list

    def identify_tsing(self, cards_list, max_using_joker):
        num_dict = self.cards_num_dict(cards_list)
        tsing_list, joker_list = [[]], num_dict['15'] + num_dict['16']
        use_joker_num = min(max_using_joker, len(joker_list))
        for i in range(3, 15):
            k = len(num_dict[str(i)])
            if k == 5:
                tsing_list.append(num_dict[str(i)])
            elif k > 5:
                # todo:
                # print(f'{Number[i-2]}有{k}张，{Number[i-2]}清有多种可能，暂时只随机选取一种')
                tsing_list.append(num_dict[str(i)][:5])
            elif k < 5 <= k + use_joker_num:
                tsing, copy_joker = num_dict[str(i)], joker_list.copy()
                for _ in range(5-k):
                    tsing.append(copy_joker.pop(0))
                tsing_list.append(tsing)
        return tsing_list

    def identify_tuo(self, cards_list, max_using_joker):
        num_dict = self.cards_num_dict(cards_list)
        tuo_list, joker_list = [[]], num_dict['15'] + num_dict['16']
        use_joker_num = min(max_using_joker, len(joker_list))
        for i in range(3, 15):
            k = len(num_dict[str(i)])
            if k == 4:
                tuo_list.append(num_dict[str(i)])
            elif k > 4:
                return None
            elif k < 4 <= k + use_joker_num:
                tuo, copy_joker = num_dict[str(i)], joker_list.copy()
                for _ in range(4 - k):
                    tuo.append(copy_joker.pop(0))
                tuo_list.append(tuo)
        return tuo_list

    def identify_typing(self, card_typing, cards_list):
        if card_typing == 'Tsing':
            return self.identify_tsing(cards_list=cards_list, max_using_joker=2)
        elif card_typing == 'StraightFlush':
            return self.identify_straight_flush(cards_list=cards_list, max_using_joker=2)
        elif card_typing == 'Tuo':
            return self.identify_tuo(cards_list=cards_list, max_using_joker=2)
        elif card_typing == 'Flush':
            return self.identify_flush(cards_list=cards_list, max_using_joker=2)
        elif card_typing == 'Straight':
            return self.identify_straight(cards_list=cards_list, max_using_joker=2)
        else:
            raise ValueError(f'Unknown 5-Cards-Typing: {card_typing}')

    def get_5_typing_plans(self, card_typing, current_plan_list):
        n, max_n = 0, 5
        while n < max_n:
            result_plan_list = []
            for current_plan in current_plan_list:
                if current_plan[f'{card_typing}-End-Label'] is True:
                    result_plan_list.append(deepcopy(current_plan))
                else:
                    typing_list = self.identify_typing(card_typing, current_plan['else'])
                    if typing_list is None:
                        continue
                    for p in typing_list:
                        if len(p) == 0:
                            new_plan = deepcopy(current_plan)
                            new_plan[f'{card_typing}-End-Label'] = True
                            result_plan_list.append(new_plan)
                        else:
                            if len(current_plan[card_typing]) == 0 or p[0].num >= current_plan[card_typing][-1][0].num:
                                new_plan = deepcopy(current_plan)
                                new_plan[card_typing].append(p)
                                new_plan = self.update_plan_else(new_plan, p)
                                result_plan_list.append(new_plan)
            current_plan_list = result_plan_list
            n += 1
        return current_plan_list

    def finish_tuo(self, current_plan):
        current_plan_list = [current_plan]
        k = len(current_plan['Tuo'])
        n, max_n = 0, k
        while n < max_n:
            result_plan_list = []
            for current_plan in current_plan_list:
                num_dict = self.cards_num_dict(current_plan['else'])
                raw_single = [p for p in current_plan['else'] if 3 <= p.num <= 14 and len(num_dict[str(p.num)]) == 1]
                if len(raw_single) >= k:
                    single = raw_single
                else:
                    single = [p for p in current_plan['else'] if 3 <= p.num <= 14]
                for p in single:
                    if n > 0 and p.num < current_plan['Tuo'][n-1][-1].num:
                        continue
                    new_plan = deepcopy(current_plan)
                    new_plan['Tuo'][n].append(p)
                    new_plan = self.update_plan_else(new_plan, [p])
                    result_plan_list.append(new_plan)
            current_plan_list = result_plan_list
            n += 1
        return current_plan_list

    def get_else_typing_plans(self, current_plan_list):
        result_plan_list = []
        for current_plan in current_plan_list:
            result_plan_list.extend(self.finish_tuo(current_plan))
        current_plan_list = result_plan_list
        result_plan_list = []
        for current_plan in current_plan_list:
            num_dict = self.cards_num_dict(current_plan['else'])
            current_plan.update({'RedJoker': num_dict['16'], 'BlackJoker': num_dict['15'], 'Trump': num_dict['2']})
            waste_flag = False
            for i in range(3, 15):
                k = len(num_dict[str(i)])
                if k >= 4:
                    waste_flag = True
                    break
                elif k == 3:
                    current_plan['Triple'].append(num_dict[str(i)])
                elif k == 2:
                    current_plan['Pair'].append(num_dict[str(i)])
                elif k == 1:
                    current_plan['Single'].append(num_dict[str(i)][0])
            if waste_flag is False:
                result_plan_list.append(current_plan)
        return result_plan_list

    def score_plan(self, mode):
        for plan in self.plan_list:
            if mode == 'score':
                score = 10 * len(plan['RedJoker']) + 8 * len(plan['BlackJoker']) + 7 * len(plan['Trump'])
                score += 2 * len([p for p in plan['Single'] if 13 <= p.num <= 14]) \
                    + 1 * len([p for p in plan['Single'] if 8 <= p.num <= 12])
                score += 2 * (8 * len([p for p in plan['Pair'] if p[0].num == 14]) +
                              5 * len([p for p in plan['Pair'] if 11 <= p[0].num <= 13]) +
                              2 * len([p for p in plan['Pair'] if 7 <= p[0].num <= 10]))
                score += 3 * (9 * len([p for p in plan['Triple'] if p[0].num == 14]) +
                              3 * len([p for p in plan['Triple'] if 11 <= p[0].num <= 13]) +
                              2 * len([p for p in plan['Triple'] if 7 <= p[0].num <= 10]))
                score += 5 * (10 * len([p for p in plan['Tsing'] if p[0].num > 10]) +
                              9 * len([p for p in plan['Tsing'] if p[0].num <= 10]) +
                              8 * len(plan['StraightFlush']) +
                              5 * len([p for p in plan['Tuo'] if p[0].num >= 11]) +
                              2 * len([p for p in plan['Tuo'] if 7 <= p[0].num <= 10]) +
                              1 * len([p for p in plan['Tuo'] if p[0].num <= 6]))
                plan['score'] = score
            elif mode == 'less_single':
                plan['score'] = -len(plan['Single'])
            elif mode == 'less_round':
                plan['score'] = -sum([len(plan[p]) for p in ['Single', 'Pair', 'Triple', 'Tsing', 'StraightFlush',
                                                             'Tuo', 'Flush', 'Straight']])
        self.plan_list.sort(key=lambda x: x['score'], reverse=True)

    def plan_hands(self, cards_list=None):
        cards_list = self.cards_list if cards_list is None else cards_list
        basic_plan = {'Tsing': [], 'StraightFlush': [], 'Tuo': [], 'FullHouse': [], 'Flush': [], 'Straight': [],
                      'Tsing-End-Label': False, 'StraightFlush-End-Label': False, 'Tuo-End-Label': False,
                      'FullHouse-End-Label': False, 'Flush-End-Label': False, 'Straight-End-Label': False,
                      'Triple': [], 'Pair': [], 'Single': [], 'else': cards_list}
        current_plan_list = self.get_5_typing_plans(card_typing='Tsing', current_plan_list=[basic_plan])
        current_plan_list = self.get_5_typing_plans(card_typing='StraightFlush', current_plan_list=current_plan_list)
        current_plan_list = self.get_5_typing_plans(card_typing='Tuo', current_plan_list=current_plan_list)
        current_plan_list = self.get_5_typing_plans(card_typing='Flush', current_plan_list=current_plan_list)
        current_plan_list = self.get_5_typing_plans(card_typing='Straight', current_plan_list=current_plan_list)
        current_plan_list = self.get_else_typing_plans(current_plan_list)
        self.plan_list = current_plan_list
        best_plan_pool = []
        for mode in ['score', 'less_single', 'less_round']:
            self.score_plan(mode)
            best_plan_pool.extend(self.plan_list[:2])
        self.plan_list = best_plan_pool

    def show_plan(self):
        for i, plan in enumerate(self.plan_list):
            print(f"------{i}号配牌方案------")

            for key in plan:
                if 'Label' in key or key in ['score', 'else'] or len(plan[key]) == 0:
                    continue
                print(key, plan[key])


class WildEscapeGame:
    def __init__(self):
        self.deck = Deck(n=3)
        self.deck.shuffle()
        self.players = [Player(position=i) for i in range(6)]

    def deal_deck(self):
        for i, person in enumerate(self.players):
            person.set_hands(self.deck.cards_list[i*27:(i+1)*27])


if __name__ == '__main__':

    game = WildEscapeGame()
    game.deal_deck()
    for player in game.players:
        print(f"######{player.position}号选手#######")
        policy = WildEscapePolicy(player.hands)
        policy.plan_hands()
        policy.show_plan()
        print("####################")
        break
