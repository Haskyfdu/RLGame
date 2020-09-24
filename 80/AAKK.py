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


class Player80:
    def __init__(self, hands=None, bookmaker='opponent', trump_suit=None, trump_num=None,):
        if hands is None:
            poker = Deck80()
            poker.shuffle()
            self.me = poker.deck[0:25]
            self.opponent = poker.deck[25:50]
            self.previous = poker.deck[50:75]
            self.next = poker.deck[75:100]
            self.final_cards = poker.deck[100:]
            self.hands = None
        else:
            self.hands = hands

        if bookmaker == 'opponent':
            self.opponent += self.final_cards
        elif bookmaker == 'previous':
            self.previous += self.final_cards
        elif bookmaker == 'next':
            self.next += self.final_cards
        elif bookmaker == 'me':
            self.me += self.final_cards
        else:
            raise ValueError('Unknown Bookmaker!')

        self.trump_suit = trump_suit
        self.trump_num = trump_num
        self.score_in_hands = 0
        self.sorted_hands = None
        self.play_card = None

        self.opponent_info = {'RunOut': [], 'PlayedCards': []}
        self.previous_info = {'RunOut': [], 'PlayedCards': []}
        self.next_info = {'RunOut': [], 'PlayedCards': []}

    def sort_hands(self,  player='me'):
        if player == 'me':
            self.hands = self.me
        elif player == 'previous':
            self.hands = self.previous
        elif player == 'next':
            self.hands = self.next
        elif player == 'opponent':
            self.hands = self.opponent
        else:
            raise ValueError('Unknown Player!')
        self.score_in_hands = 0
        for card in self.hands:
            if card.num == self.trump_num:
                card.value = 500
            if card.suit == self.trump_suit:
                card.value += 200

            if card.num == 5:
                self.score_in_hands += 5
            elif card.num == 10 or card.num == 13:
                self.score_in_hands += 10
        trump = [p for p in self.hands if p.value >= 101]
        club = [p for p in self.hands if 100 >= p.value >= 61]
        diamond = [p for p in self.hands if 60 >= p.value >= 41]
        heart = [p for p in self.hands if 40 >= p.value >= 21]
        spade = [p for p in self.hands if 20 >= p.value >= 1]
        hands = [trump, club, diamond, heart, spade]
        name = ['Trump', 'Club', 'Diamond', 'Heart', 'Spade']
        self.sorted_hands = {}
        for i in range(5):
            h = hands[i]
            h.sort(key=lambda p: p.value, reverse=True)
            n = name[i]
            self.sorted_hands[n] = h

    def show_hands(self, player='me'):
        self.sort_hands(player)
        name = ['Trump', 'Club', 'Diamond', 'Heart', 'Spade']
        print_str_list = ['Trump:     ', 'Club:      ', 'Diamond:   ',
                          'Heart:     ', 'Spade:     ']
        for i in range(5):
            n = name[i]
            h = self.sorted_hands[n]
            print(print_str_list[i], h)
        print('Score: ', self.score_in_hands)

    def bury(self):
        pass

    def play(self, round_card):
        if len(round_card) == 0:
            self.policy1()
        elif len(round_card) == 1:
            self.policy2(round_card)
        elif len(round_card) == 2:
            self.policy3(round_card)
        elif len(round_card) == 3:
            self.policy4(round_card)

    def read_round_card(self, round_card):
        pass

    def policy1(self):
        pass

    def policy2(self, round_card):
        pass

    def policy3(self, round_card):
        pass

    def policy4(self, round_card):
        pass

    def ans(self, round_card):
        self.play(round_card)
        print(self.play_card)


if __name__ == '__main__':

    a = Player80()
    a.show_hands('Spade', 10, 'opponent')
    print('############################')
    a.show_hands('Spade', 10, 'previous')
    print('############################')
    a.show_hands('Spade', 10, 'me')
    print('############################')
    a.show_hands('Spade', 10, 'next')


