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
        input_str = input_str.replace(' ', '')
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

    def identify_typing_main(self, card_typing, cards_list):
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
                    typing_list = self.identify_typing_main(card_typing, current_plan['else'])
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

    @staticmethod
    def get_full_house_plans(current_plan):
        triple_list = current_plan['Triple']
        pair_list = current_plan['Pair']
        n = min(len(triple_list), len(pair_list))
        result_plan_list = []
        for i in range(n+1):
            new_plan = deepcopy(current_plan)
            for _ in range(i):
                new_plan['FullHouse'].append(new_plan['Triple'].pop(0) + new_plan['Pair'].pop(0))
            result_plan_list.append(new_plan)
        return result_plan_list

    @staticmethod
    def get_trump_plan(current_plan):
        trump_and_joker = current_plan['RedJoker'] + current_plan['BlackJoker'] + current_plan['Trump']
        n = len(trump_and_joker)
        ai_num = []
        for a5 in range(n//5+1):
            n -= 5*a5
            for a3 in range(n//3+1):
                n -= 3*a3
                for a2 in range(n//2+1):
                    ai_num.append([a5, a3, a2])
        result_plan_list = []
        for ai_plan in ai_num:
            a5, a3, a2 = ai_plan
            new_plan = deepcopy(current_plan)
            using_trump = deepcopy(trump_and_joker)
            for _ in range(a5):
                new_plan['Tsing'].append(using_trump[-5:])
                using_trump = using_trump[:-5]
            for _ in range(a3):
                new_plan['Triple'].append(using_trump[-3:])
                using_trump = using_trump[:-3]
            for _ in range(a2):
                new_plan['Pair'].append(using_trump[-2:])
                using_trump = using_trump[:-2]
            new_plan['Single'].extend(using_trump)
            result_plan_list.append(new_plan)
        return result_plan_list

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
        current_plan_list = result_plan_list
        result_plan_list = []
        for current_plan in current_plan_list:
            for new_plan in self.get_full_house_plans(current_plan):
                result_plan_list.extend(self.get_trump_plan(new_plan))
        return result_plan_list

    def score_plan(self, priority):
        for plan in self.plan_list:
            special_score = {'Single': {'15': 0.24, '16': 0.3, '17': 0.5},
                             'Pair': {'15': 0.5, '16': 0.6, '17': 0.6},
                             'Triple': {'15': 0.5, '16': 0.6, '17': 0.6}}
            score = {'Tsing': sum([(55+p[0].value-2)/68 - 0.4 for p in plan['Tsing']]),
                     'StraightFlush': sum([(45+min([p[i].value-i for i in range(5)])-2)/68 - 0.5
                                           for p in plan['StraightFlush']]),
                     'Tuo': sum([(32+p[0].value-2)/68 - 0.5 for p in plan['Tuo']]),
                     'FullHouse': sum([(20+p[0].value-2)/68 - 0.5 for p in plan['Tsing']]),
                     'Flush': sum([(10 + p[-1].value - 4) / 68 - 0.5 for p in plan['Flush']]),
                     'Straight': sum([min([p[i].value - i for i in range(5)]) / 68 - 0.5
                                      for p in plan['Straight']]),
                     'Triple': sum([(p[0].value-3) / 14 - 0.5 if p[0].value <= 14 else
                                    special_score['Triple'][str(p[0].value)] for p in plan['Triple']]),
                     'Pair': sum([(p[0].value-3) / 14 - 0.5 if p[0].value <= 14 else
                                  special_score['Pair'][str(p[0].value)] for p in plan['Pair']]),
                     'Single': sum([(p.value-3) / 15 - 0.66 if p.value <= 14 else
                                    special_score['Single'][str(p.value)] for p in plan['Single']])}
            plan['score'] = {'All': round(sum(score.values()), 2),
                             '5': round(sum([score[p] for p in ['Tsing', 'StraightFlush', 'Tuo', 'FullHouse',
                                                                'Flush', 'Straight']]), 2),
                             '3': round(score['Triple'], 2),
                             '2': round(score['Pair'], 2),
                             '1': round(score['Single'], 2)}
        self.plan_list.sort(key=lambda x: x['score']['All'] + x['score'][priority], reverse=True)

    def plan_hands(self, cards_list=None, priority='5'):
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
        self.score_plan(priority)

    def show_plan(self, top_n):
        for i, plan in enumerate(self.plan_list[:top_n]):
            print(f"------{i+1}号配牌方案------")
            print(plan['score'])
            for key in plan:
                if 'Label' in key \
                        or key in ['score', 'else', 'RedJoker', 'BlackJoker', 'Trump'] \
                        or len(plan[key]) == 0:
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


def main():
    print('欢迎使用大怪路子配牌助手1.0～')
    print('字符串识别规则: ')
    print('1、花色用SHDC进行表示: ♠黑桃-S   ♥红桃-H   ♦方片-D   ♣草花-C')
    print('2、相同花色的牌可以连成一串输入, 点数用数字/字母表示, 注意其中10用T表示: 123456789TJQKA 【A用1或者A表示均可】')
    print('3、大小鬼用RJ/BJ表示')
    print('4、字母大小写均可, 不同花色之间可以空格, 同一花色也可以多段输入【每一段都需要声明花色】')
    print('例子: RJ bjS334556H4458JJ D99725K CT542 s789')
    policy = WildEscapePolicy()
    policy.identify_cards_from_string('RJ BJ S334556789 H4458JJ D99725K CT542')
    policy.identify_cards_from_string(input('请输入您的手牌:'))
    policy.plan_hands(priority='5')
    policy.show_plan(top_n=5)


if __name__ == '__main__':

    # game = WildEscapeGame()
    # game.deal_deck()
    # policy_test = WildEscapePolicy(cards_list=game.players[0].hands)
    # policy_test.plan_hands(priority='5')
    # policy_test.show_plan(top_n=5)
    main()
