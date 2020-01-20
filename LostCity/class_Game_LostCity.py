from LostCity.class_Deck_LostCity import DeckLostCity


class LostCity:
    def __init__(self, num_learning_rounds, learner=None, report_every=100):
        self.cards_on_field = []
        self.player1 = None
        self.player2 = None

    def reset(self):
        deck = DeckLostCity(color_number=3, double_number=2, max_number=5)
        self.player1 = None
        self.player2 = None