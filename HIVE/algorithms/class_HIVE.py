import random
import matplotlib.pyplot as plt


from HIVE.algorithms.class_Player import Player


class HIVE:
    def __init__(self):
        self.Black = Player('Black')
        self.White = Player('White')
        self.winner = None
        self.chessboard = []
        self.turn = 0

    def show(self):
        self.chessboard.sort(key=lambda x: x.layer)
        for piece in self.chessboard:
            piece.show()
        plt.axis('equal')
        plt.show()

    def next_turn(self):
        player = self.White if self.turn % 2 == 0 else self.Black
        opponent = self.White if self.turn % 2 == 1 else self.Black
        action_pool = player.enumerate_action_pool(self.chessboard)
        if len(action_pool) >= 0:
            action = player.best_action(self.chessboard, opponent, action_pool)
            player.play(action, self.chessboard)
        self.turn += 1

    def check_win(self):
        if self.White.lose(self.chessboard):
            if self.Black.lose(self.chessboard):
                self.winner = 'Both'
            else:
                self.winner = 'Black'
        if self.Black.lose(self.chessboard):
            self.winner = 'White'

    def play(self):
        while self.winner is None and self.turn < 60:
            self.next_turn()
            self.check_win()
            print(self.turn)
            self.show()


if __name__ == '__main__':

    Game = HIVE()
    Game.play()
