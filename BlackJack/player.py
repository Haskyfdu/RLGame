class Player:
    def __init__(self):
        self._hand = []
        self._original_showing_value = 0

    def get_hand(self):
        return self._hand

    def get_action(self):
        if self.get_hand_value() < 17:
            return 'hit'
        else:
            return 'stay'

    def get_hand_value(self):
        return sum(self._hand)

    def get_showing_value(self):
        showing = self._hand[1]
        self._original_showing_value = showing
        return showing

    def get_original_showing_value(self):
        return self._original_showing_value

    def hit(self, deck):
        card_value = deck.draw()
        self._hand.append(card_value)

    @staticmethod
    def stay():
        return True

    def reset_hand(self):
        self._hand = []

    def update(self):
        pass

