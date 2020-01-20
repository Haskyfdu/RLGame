import random

# Color = ['Red', 'Blue', 'White', 'Yellow', 'Green']
Color = 'RBWYG'


class DeckLostCity:
    def __init__(self, color_number=5, double_number=3, max_number=10):
        self.color_number = color_number
        self.double_number = double_number
        self.max_number = max_number
        self.cards = []
        for color_id in range(self.color_number):
            self.cards.extend([Color[color_id]+str(0)]*self.double_number +
                              [Color[color_id]+str(p) for p in range(self.max_number)])
        random.shuffle(self.cards)
        # print(self.cards)

    def draw_n(self, draw_number=1):
        draw_cards = []
        for i in range(draw_number):
            draw_cards.append(self.cards.pop())
        return draw_cards

    def get_left_cards_num(self):
        return len(self.cards)


if __name__ == '__main__':

    deck = DeckLostCity(color_number=3, double_number=2, max_number=5)
