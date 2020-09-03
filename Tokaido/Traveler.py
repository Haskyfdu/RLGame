import random


class Traveler:
    def __init__(self):
        self.coins = 0
        self.score = 0
        self.souvenir_cards = []
        self.sea = 0
        self.mountain = 0
        self.paddy = 0
        self.donated = 0
        self.hot_spring = 0
        self.location = 0

    def visit_farm(self):
        self.coins += 3

    def visit_hot_spring(self):
        self.hot_spring += 1
        self.score += random.randint(2, 3)  # todo: limited hot spring cards

    def visit_village(self):
        if self.coins >= 1:
            souvenir_cards = [0, 1, 2]  # todo: souvenir cards
            self.pick_souvenir_cards(souvenir_cards)
        else:
            raise ValueError('A traveler must have at least 1 coin to stop in a Village, '
                             'but he is not required to purchase any souvenirs.')

    def pick_souvenir_cards(self, souvenir_cards):
        add_score = 0
        pick = []
        cost = 0
        # todo: pick card by smart rule
        self.souvenir_cards.extend(pick)
        self.coins -= cost
        self.score += add_score

    def visit_sea(self):
        self.sea += 1
        self.score += self.sea

    def visit_mountain(self):
        self.mountain += 1
        self.score += self.mountain

    def visit_paddy(self):
        self.paddy += 1
        self.score += self.paddy

    def visit_temple(self, n):
        if n in [1, 2, 3]:
            self.coins -= n
            self.score += n
            self.donated += n
        else:
            raise ValueError('A traveler who stops on a Temple space must donate at least '
                             '1 coin as an offering and cannot donate more than 3 coins.')

    def visit_encounters(self):
        r = random.randint(0, 4)
        encounter = ['Shokunin', 'Annaibito', 'Samurai', 'Kuge', 'Miko'][r]
        # todo: limit cards
        if encounter == 'Shokunin':
            souvenir_card = random.randint(2)
            self.score += 0
            self.souvenir_cards.append(souvenir_card)  # todo: village
        elif encounter == 'Annaibito':
            self.sea += 1
            self.score += self.sea   # todo: pick sea?
        elif encounter == 'Samurai':
            self.score += 3
        elif encounter == 'Kuge':
            self.coins += 3
        elif encounter == 'Miko':
            self.donated += 1
            self.score += 1
        else:
            raise ValueError('Unknown Encounter!')

    def arrive_inns(self, meal_cards):
        self.pick_meal_cards(meal_cards)

    def pick_meal_cards(self, meal_cards):
        pick = meal_cards[0]
        self.coins -= pick.price
        self.score += 6
        # todo: choose food

    def achievement(self):
        self.score += 3

    def move(self, n):
        self.location += n


class OldMan(Traveler):
    def __init__(self):
        super().__init__()
        self.coins = 6

    def visit_hot_spring(self):
        super().visit_hot_spring()
        self.score += 1

    def achievement(self):
        super().achievement()
        self.score += 1


class Priest(Traveler):
    def __init__(self):
        super().__init__()
        self.coins = 8

    def visit_temple(self, n):
        super().visit_temple(n)
        self.score += 1
        self.donated += 1


class StreetEntertainer(Traveler):
    def __init__(self):
        super().__init__()
        self.coins = 5

    def visit_encounters(self):
        self.coins += 1
        self.score += 1
        super().visit_encounters()
