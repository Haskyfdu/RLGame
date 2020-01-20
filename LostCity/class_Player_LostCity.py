# Color = ['Red', 'Blue', 'White', 'Yellow', 'Green']
Color = 'RBWYG'


class PlayerLostCity:
    def __init__(self):
        self.cards_in_hand = []
        self.cards_on_field_own = {}
        self.cards_on_field_opponent = {}
        self.fold_deck = {}
        self.pass_card_num = 0

    def get_hand(self):
        return self.cards_in_hand

    def draw_n(self, deck, draw_n=1):
        self.cards_in_hand.extend(deck.draw_n(draw_number=draw_n))

    def play(self, play_card):
        if play_card in self.cards_in_hand:
            card_index = self.cards_in_hand.index(play_card)
            del self.cards_in_hand[card_index]
        else:
            raise ValueError('You can‘t play the card which is not in your hand')
        if play_card[0] in self.cards_on_field_own:
            self.cards_on_field_own[play_card[0]].append(play_card)
        else:
            self.cards_on_field_own.update({play_card[0]: [play_card]})

    def fold(self, fold_card):
        if fold_card in self.cards_in_hand:
            card_index = self.cards_in_hand.index(fold_card)
            del self.cards_in_hand[card_index]
        else:
            raise ValueError('You can‘t fold the card which is not in your hand')
        if fold_card[0] in self.fold_deck:
            self.fold_deck[fold_card[0]].append(fold_card)
        else:
            self.fold_deck.update({fold_card[0]: [fold_card]})

    def pick(self, pick_card):
        if pick_card[0] in self.fold_deck and len(self.fold_deck[pick_card[0]]) > 0 \
                and pick_card == self.fold_deck[pick_card[0]].pop():
            self.cards_in_hand.append(pick_card)
        else:
            raise ValueError('You can only pick the card which is the top card of fold deck ')