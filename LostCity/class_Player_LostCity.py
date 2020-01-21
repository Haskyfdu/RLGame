Color = ['Red', 'Blue', 'White', 'Yellow', 'Green']


class PlayerLostCity:
    def __init__(self):
        self.cards_in_hand = []
        self.cards_on_field_own = {}
        self.cards_on_field_opponent = {}
        self.fold_deck = {}
        self.pass_card_num = 0
        self.points_dict_own = {}
        self.points_dict_opponent = {}
        self.points_dict_hand = {}
        self.points_dict_left = {}
        self.score = 0

    def get_hand(self):
        return self.cards_in_hand

    def get_points_dict_own(self):
        self.points_dict_own = {color: sum(self.cards_on_field_own[color]).num
                                for color in self.cards_on_field_own}

    def get_points_dict_opponent(self):
        self.points_dict_opponent = {color: sum(self.cards_on_field_opponent[color]).num
                                     for color in self.cards_on_field_opponent}

    def get_points_dict_hand(self):
        for card in self.cards_in_hand:
            if card.color not in self.cards_on_field_own \
                    or card >= self.cards_on_field_own[card.color][-1]:
                if card.color in self.points_dict_hand:
                    self.points_dict_hand[card.color] += card.num
                else:
                    self.points_dict_hand[card.color] = card.num

    def get_points_dict_left(self, color_num, max_number):
        for p in range(color_num):
            if Color[p] not in self.cards_on_field_own:
                max_number_now_own = 0
            else:
                max_number_now_own = self.cards_on_field_own[Color[p]][-1]

    def draw_n(self, deck, draw_n=1):
        self.cards_in_hand.extend(deck.draw_n(draw_number=draw_n))
        self.pass_card_num += draw_n

    def play(self, play_card):
        if play_card in self.cards_in_hand:
            if play_card.color not in self.cards_on_field_own \
                    or play_card >= self.cards_on_field_own[play_card.color][-1]:
                card_index = self.cards_in_hand.index(play_card)
                del self.cards_in_hand[card_index]
            else:
                raise ValueError('You can only paly the card bigger than the card on field.')
        else:
            raise ValueError('You can‘t play the card which is not in your hand.')
        if play_card.color in self.cards_on_field_own:
            self.cards_on_field_own[play_card.color].append(play_card)
        else:
            self.cards_on_field_own.update({play_card.color: [play_card]})

    def fold(self, fold_card):
        if fold_card in self.cards_in_hand:
            card_index = self.cards_in_hand.index(fold_card)
            del self.cards_in_hand[card_index]
        else:
            raise ValueError('You can‘t fold the card which is not in your hand.')
        if fold_card.color in self.fold_deck:
            self.fold_deck[fold_card.color].append(fold_card)
        else:
            self.fold_deck.update({fold_card.color: [fold_card]})

    def pick(self, pick_card):
        if pick_card.color in self.fold_deck and len(self.fold_deck[pick_card.color]) > 0 \
                and pick_card == self.fold_deck[pick_card.color].pop():
            self.cards_in_hand.append(pick_card)
        else:
            raise ValueError('You can only pick the card which is the top card of fold deck.')
