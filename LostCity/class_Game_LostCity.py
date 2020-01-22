from LostCity.class_Deck_LostCity import DeckLostCity
from LostCity.class_Player_LostCity import PlayerLostCity


class LostCity:
    def __init__(self, color_number, double_number, max_number):
        self.player1 = None
        self.player2 = None
        self.players = [self.player1, self.player2]
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
        self.players = [self.player1, self.player2]
        self.player1.draw_n(deck=self.deck, draw_n=8)
        self.player2.draw_n(deck=self.deck, draw_n=8)

    def get_actions(self):
        pass
    # todo

    def get_actions_step1(self, player_id):
        handcards = self.players[player_id].get_hand()
        for card in handcards:
            pass
        # todo





    def step(self, action):
        pass
