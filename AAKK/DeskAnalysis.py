from AAKK.HandsAnalysis import cards_basic_pattern_analysis
from AAKK.SetGame import GameSet80, Cards


Suit_Dict = {'S': 'Spade', 'H': 'Heart', 'D': 'Diamond', 'C': 'Club', 'T': 'Trump'}
# upper()


game = GameSet80(bookmaker='opponent', trump_suit='Spade', trump_num=2)
game.sort_hands()


def input_cards(cards_str: str, cards=None, deck_num=2):
    if cards is None:
        cards = []
    cards_str.upper()
    for c in ['RJ', 'BJ']:
        while c in cards_str:
            k = cards_str.find(c)
            if k != -1:
                cards_str = cards_str[:k]+cards_str[k+2]
                cards.append(Cards('RedJoker'))
    suit, card_num = None, {}
    for i in range(len(cards_str)):
        if cards_str[i] in 'SHDC':
            suit = Suit_Dict[cards_str[i]]
            continue
        elif cards_str[i] in '234567890JQKA':
            card_name = suit+cards_str[i]
            if card_name in card_num:
                if card_num[card_name] == deck_num:
                    raise ValueError('only ' + str(deck_num) + ' decks.')
                else:
                    card_num[card_name] += 1
            else:
                card_num[card_name] = 1
            num = '234567890JQKA'.index(cards_str[i])+2
        else:
            print(cards_str[i])
            raise ValueError('cards_str input error.')
        if suit is None:
            raise ValueError('cards_str input error.')
        else:
            cards.append(Cards(suit, num))
    return cards


ans = input_cards('HA2724KK9988766JJ')
print(ans)

pattern = cards_basic_pattern_analysis(ans, 5, 'Spade')


def round_analysis(round_cards, desk_info, hands, trump_num, trump_suit):
    rank = len(round_cards)
    round_cards_len = len(round_cards[0])
    if round_cards[0][0].trump:
        round_suit = 'Trump'
    else:
        round_suit = round_cards[0][0].suit
    pattern = cards_basic_pattern_analysis(round_cards[0], trump_num, trump_suit)
    if len(pattern['continuously_pairs']) > 0:
        pass
    elif len(pattern['pairs']) > 0:
        pass
    else:
        pass

