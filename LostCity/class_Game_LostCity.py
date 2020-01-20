from LostCity.class_Deck_LostCity import DeckLostCity
from LostCity.class_Player_LostCity import PlayerLostCity


class LostCity:
    def __init__(self, color_number, double_number, max_number):
        self.player1 = None
        self.player2 = None
        self.color_number = color_number
        self.double_number = double_number
        self.max_number = max_number
        self.deck = []

    def reset(self):
        self.deck = DeckLostCity(color_number=self.color_number,
                                 double_number=self.double_number,
                                 max_number=self.max_number)
        self.player1 = PlayerLostCity()
        self.player2 = PlayerLostCity()
        self.player1.draw_n(deck=self.deck, draw_n=8)
        self.player2.draw_n(deck=self.deck, draw_n=8)

    def get_action(self):
        pass

    def step(self, action):
        pass
