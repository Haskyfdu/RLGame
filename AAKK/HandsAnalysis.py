from AAKK.SetGame import GameSet80

Suit_list = ['Spade', 'Heart', 'Diamond', 'Club']
Suit_dict = {'Spade': '♠', 'Heart': '♥', 'Diamond': '♦', 'Club': '♣',
             'RedJoker': 'RJ', 'BlackJoker': 'BJ'}
Number = ['2', '3', '4', '5', '6', '7', '8',
          '9', '10', 'J', 'Q', 'K', 'A', '']

game = GameSet80(bookmaker='opponent', trump_suit='Spade', trump_num=2)
game.sort_hands()
game.show_hands()

# game.bury({'Club': [1, 2, 3], 'Diamond': [1, 2, 3, 4], 'Heart': [-1]})
# game.show_hands()


def cards_basic_pattern_analysis(cards, trump_num, trump_suit):
    pairs = []
    for i in range(len(cards)-1):
        if cards[i] == cards[i+1]:
            pairs.append(cards[i])
    continuously_pairs = []
    for i in range(len(pairs)-1):
        begin_card = pairs[i]
        p = 0
        checking_result = [begin_card]
        while i+p < len(pairs)-1:
            card = pairs[i+p]
            next_card = pairs[i+p+1]
            checking_result.append(next_card)
            k = card.num
            j = next_card.num
            if (k - 1 == j
                    or k - 1 == trump_num == j + 1
                    or (j == 14 and k == trump_num and card.suit != trump_suit)
                    or (k == j == trump_num and card.suit == trump_suit)
                    or (card.suit == 'RedJoker' and next_card.suit == 'BlackJoker')
                    or (card.suit == 'BlackJoker' and next_card.suit == trump_suit and j == trump_num)):
                continuously_pairs.append(checking_result.copy())
                p += 1
            else:
                break
    return {'pairs': pairs,
            'continuously_pairs': continuously_pairs}


def hands_pattern_analysis(hands, trump_num, trump_suit):
    trump_len = len(hands['Trump'])
    pairs = {}
    continuously_pairs = {}
    for suit in hands:
        r = cards_basic_pattern_analysis(hands[suit], trump_num, trump_suit)
        pairs[suit], continuously_pairs[suit] = r['pairs'], r['continuously_pairs']
    return {'trump_len': trump_len,
            'pairs': pairs,
            'continuously_pairs': continuously_pairs}
