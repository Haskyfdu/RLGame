# Color = ['Red', 'Blue', 'White', 'Yellow', 'Green']
Color = 'RBWYG'


class SimpleLostCity:
    def __init__(self, cards_on_field, cards_in_hand, color_number=5, double_number=3, max_number=10):
        self.cards_on_field = cards_on_field
        self.cards_in_hand = cards_in_hand
        self.color_number = color_number
        self.double_number = double_number
        self.max_number = max_number
        self.opponent_cards = {}
        self.my_cards = {}
        self.fold_cards = {}
        self.hand_cards = {}
        self.cards_used = 0
        for color_id in range(self.color_number):
            self.opponent_cards.update({Color[color_id]: cards_on_field[Color[color_id]]['opponent']})
            self.cards_used += len(cards_on_field[Color[color_id]]['opponent'])
            self.my_cards.update({Color[color_id]: cards_on_field[Color[color_id]]['my']})
            self.cards_used += len(cards_on_field[Color[color_id]]['my'])
            self.fold_cards.update({Color[color_id]: cards_on_field[Color[color_id]]['fold']})
            self.cards_used += len(cards_on_field[Color[color_id]]['fold'])
            self.hand_cards.update({Color[color_id]: cards_in_hand[Color[color_id]]})
        self.action = {}
        self.cards_num_all = self.color_number*(self.max_number+self.double_number)
        self.cards_used += 8

    def ponder(self):
        for color_id in range(self.color_number):
            if len(self.my_cards[Color[color_id]]) == 0:
                pass
            else:
                pass




