import random

Suit_list = ['Spade', 'Heart', 'Diamond', 'Club']
Suit_dict = {'Spade': '♠', 'Heart': '♥', 'Diamond': '♦', 'Club': '♣',
             'RedJoker': 'RJ', 'BlackJoker': 'BJ'}
Number = ['2', '3', '4', '5', '6', '7', '8',
          '9', '10', 'J', 'Q', 'K', 'A', '']


class Cards:
    def __init__(self, suit, num=15):
        if suit in Suit_list:
            self.suit = suit
            self.num = num
            self.value = num + 20*Suit_list.index(suit)
        elif suit in ['RedJoker', 'BlackJoker']:
            self.suit = suit
            self.num = num
            self.value = 1000 - ['RedJoker', 'BlackJoker'].index(suit)
        else:
            raise ValueError('Unknown Suit!')

    def __eq__(self, other):
        if self.suit == other.suit and self.num == other.num:
            return True
        else:
            return False

    def __repr__(self):
        return Suit_dict[self.suit]+Number[self.num-2]


class Deck80:
    def __init__(self):
        self.deck = []
        for suit in Suit_list:
            for num in range(2, 15):
                self.deck.extend([Cards(suit, num), Cards(suit, num)])
        self.deck.extend([Cards('RedJoker'), Cards('RedJoker'),
                          Cards('BlackJoker'), Cards('BlackJoker')])

    def shuffle(self):
        random.shuffle(self.deck)

    def __repr__(self):
        return str(self.deck)


class GameSet80:
    def __init__(self, bookmaker, trump_suit, trump_num):
        poker = Deck80()
        poker.shuffle()
        self.bookmaker = bookmaker
        self.players_hands = {'me': poker.deck[0:25],
                              'opponent': poker.deck[25:50],
                              'previous': poker.deck[50:75],
                              'next': poker.deck[75:100]}
        self.players_hands[bookmaker] += poker.deck[100:]
        self.bury_cards = None
        self.sorted_players_hands = {}
        self.score_in_hands = {}

        self.trump_suit = trump_suit
        self.trump_num = trump_num

    def sort_hands(self):
        for person in ['opponent', 'previous', 'me', 'next']:
            hands = self.players_hands[person]
            score_in_hands = 0
            for card in hands:
                if card.num == self.trump_num:
                    card.value = 500
                if card.suit == self.trump_suit:
                    card.value += 200
                if card.num == 5:
                    score_in_hands += 5
                elif card.num == 10 or card.num == 13:
                    score_in_hands += 10
            trump = [p for p in hands if p.value >= 101]
            club = [p for p in hands if 100 >= p.value >= 61]
            diamond = [p for p in hands if 60 >= p.value >= 41]
            heart = [p for p in hands if 40 >= p.value >= 21]
            spade = [p for p in hands if 20 >= p.value >= 1]
            hands = [trump, club, diamond, heart, spade]
            name = ['Trump', 'Club', 'Diamond', 'Heart', 'Spade']
            sorted_hands = {}
            for i in range(5):
                h = hands[i]
                h.sort(key=lambda p: p.value, reverse=True)
                n = name[i]
                sorted_hands[n] = h
            self.sorted_players_hands[person] = sorted_hands
            self.score_in_hands[person] = score_in_hands

    def show_hands(self):
        for person in ['opponent', 'previous', 'me', 'next']:
            name = ['Trump', 'Club', 'Diamond', 'Heart', 'Spade']
            print_str_list = ['Trump:     ', 'Club:      ', 'Diamond:   ',
                              'Heart:     ', 'Spade:     ']
            for i in range(5):
                n = name[i]
                h = self.sorted_players_hands[person][n]
                print(print_str_list[i], h)
            print('Score: ', self.score_in_hands[person])
            print('############################')

    def bury(self, bury_cards):
        self.bury_cards = bury_cards
        for suit in bury_cards:
            bury_list = bury_cards[suit]
            bury_list.reverse()
            for k in bury_list:
                del self.sorted_players_hands[self.bookmaker][suit][k]


if __name__ == '__main__':

    game = GameSet80(bookmaker='opponent', trump_suit='Spade', trump_num=2)
    game.sort_hands()
    game.show_hands()

    # game.bury({'Club': [1, 2, 3], 'Diamond': [1, 2, 3, 4], 'Heart': [-1]})
    # game.show_hands()
