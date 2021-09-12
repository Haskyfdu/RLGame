import random
from typing import List


Suit_List = ['Spade', 'Heart', 'Diamond', 'Club']

Suit_Abbreviation = {'S': 'Spade', 'H': 'Heart',
                     'D': 'Diamond', 'C': 'Club', 'T': 'Trump'}

Suit_Dict = {'Spade': '♠', 'Heart': '♥',
             'Diamond': '♦', 'Club': '♣',
             'RedJoker': 'RJ', 'BlackJoker': 'BJ'}

Number = ['2', '3', '4', '5', '6', '7', '8',
          '9', '10', 'J', 'Q', 'K', 'A', '']


class Cards:
    def __init__(self, suit, num=15):
        self.suit = suit
        self.num = num
        self.trump = False
        if suit in Suit_List:
            self.value = num + 20*Suit_List.index(suit)
        elif suit in ['RedJoker', 'BlackJoker']:
            self.value = 1000 - ['RedJoker', 'BlackJoker'].index(suit)
            self.trump = True
        else:
            raise ValueError('Unknown Suit!')

    def __eq__(self, other):
        if self.suit == other.suit and self.num == other.num:
            return True
        else:
            return False

    def __repr__(self):
        return Suit_Dict[self.suit]+Number[self.num-2]


class Deck80:
    def __init__(self):
        self.deck = []
        for suit in Suit_List:
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
        if trump_suit in Suit_List+['No Trump', 'NT', 'nt']:
            self.trump_suit = trump_suit
        elif trump_suit in 'SHDCshdc' and len(trump_suit) == 1:
            self.trump_suit = Suit_Abbreviation[trump_suit.upper()]
        else:
            raise ValueError('Unknown Trump Suit!')
        self.trump_num = trump_num
        BasicAction80.set_value(poker.deck, trump_suit=trump_suit, trump_num=trump_num)
        self.bookmaker = bookmaker
        self.players_hands = {'me': poker.deck[0:25],
                              'opponent': poker.deck[25:50],
                              'previous': poker.deck[50:75],
                              'next': poker.deck[75:100]}
        self.players_hands[bookmaker] += poker.deck[100:]
        self.bury_cards = None
        self.sorted_players_hands = {}
        self.score_in_hands = {}

    def sort_hands(self):
        for person in ['opponent', 'previous', 'me', 'next']:
            hands = self.players_hands[person]
            score_in_hands = 0
            for card in hands:
                if card.num == 5:
                    score_in_hands += 5
                elif card.num == 10 or card.num == 13:
                    score_in_hands += 10
            trump = [p for p in hands if p.trump is True]
            club = [p for p in hands if p.suit == 'Club' and p.trump is False]
            diamond = [p for p in hands if p.suit == 'Diamond' and p.trump is False]
            heart = [p for p in hands if p.suit == 'Heart' and p.trump is False]
            spade = [p for p in hands if p.suit == 'Spade' and p.trump is False]
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


class BasicAction80:
    def __init__(self, trump_suit, trump_num, cards):
        self.trump_suit = trump_suit
        self.trump_num = trump_num
        self.cards = cards

    @classmethod
    def set_value(cls, cards: List[Cards], trump_num: int, trump_suit: str):
        for card in cards:
            if card.num == trump_num:
                card.value += 500
                card.trump = True
            if card.suit == trump_suit:
                card.value += 200
                card.trump = True


if __name__ == '__main__':

    game = GameSet80(bookmaker='opponent', trump_suit='Spade', trump_num=2)
    game.sort_hands()
    game.show_hands()

    # game.bury({'Club': [1, 2, 3], 'Diamond': [1, 2, 3, 4], 'Heart': [-1]})
    # game.show_hands()
