from matplotlib import pyplot as plt
from HIVE.algorithms.class_Player import Player


class HIVE:
    def __init__(self):
        self.player1 = Player('Hasky')
        self.player2 = Player('Hattie')
        self.winner = None
        self.pieces_list = None

    def show(self):
        pass


if __name__ == '__main__':

    plt.scatter([1, 2, 3, 4], [1, 1, 1, 1], marker='h', s=15000, c='r')
    plt.scatter([1, 2], [1, 1], marker='h', s=[800] * 2, c='b')
    plt.show()
