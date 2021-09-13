from matplotlib import pyplot as plt
from HIVE.algorithms.class_Player import Player


class HIVE:
    def __init__(self):
        self.Black = Player('Black')
        self.White = Player('White')
        self.winner = None
        self.chessboard = []
        self.turn = 'White'

    def place(self, player, piece_name, location):
        if player == 'Black':
            self.Black.place(piece_name, location, self.chessboard)
        elif player == 'White':
            self.White.place(piece_name, location, self.chessboard)
        else:
            raise ValueError('Unknown Player.')

    def move(self, piece, location):
        piece.move(location, self.chessboard)

    def show(self):
        print(self.chessboard)


if __name__ == '__main__':

    Game = HIVE()

