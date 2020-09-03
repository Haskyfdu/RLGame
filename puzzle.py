from matplotlib import pyplot as plt
from typing import List

Scatter_markers = ['s', 'o', '^', '8', 'p', 'd', 'v', 'h', '>', '<']
Scatter_colors = ['b', 'g', 'r', 'm', 'y', 'k']

PieceBasicData = [[(0, 1), (0, 2), (0, 3), (-1, 2)],
                  [(0, 1), (0, 2), (-1, 1), (-2, 1)],
                  [(0, 1), (-1, 0), (1, 1), (1, 2)],
                  [(0, 1), (1, 0), (1, 1), (1, 2)],
                  [(1, 0), (1, 1), (1, 2), (1, 3)],
                  [(1, 0), (2, 0), (2, 1), (2, 2)],
                  [(0, 1), (1, 1), (1, 2), (2, 1)],
                  [(0, 1), (1, 0), (2, 0), (2, 1)],
                  [(0, 1), (0, 2), (1, 2), (-1, 2)],
                  [(0, 1), (0, 2), (1, 1), (1, 2)],
                  [(0, 1), (0, 2), (1, 2), (1, 3)],
                  [(1, 0), (1, 1), (1, 2), (2, 0)]]


class Piece:
    def __init__(self, shape_list):
        self.shape = shape_list

    def show(self, d=0):
        x = [0]
        y = [0]
        for p in self.shape:
            a, b = 0, 0
            if d == 0:
                a = p[0]
                b = p[1]
            elif d == 1:
                if p[0] > 0:
                    b -= p[0]
                else:
                    a -= p[0]
                if p[1] > 0:
                    a += p[1]
                    b -= p[1]
                else:
                    a += p[1]
            elif d == -1:
                if p[0] > 0:
                    a -= p[0]
                else:
                    b += p[0]
                if p[1] > 0:
                    a -= p[1]
                    b -= p[1]
                else:
                    a -= p[1]
            else:
                raise ValueError
            x.append(a)
            y.append(b + abs(a) * 0.5)
        plt.xlim(-4, 4)
        plt.ylim(-4, 4)
        plt.scatter(y, x, marker='s', s=[2000]*len(x))
        plt.show()


class Puzzle:
    def __init__(self, piece_list: List[Piece], q=(0, 4)):
        self.board = {}
        self.build_board()
        self.q = q
        self.board[q] = 1
        self.piece_list = piece_list

    def build_board(self):
        for i in range(-4, 5):
            for j in range(9 - abs(i)):
                key = (i, j)
                self.board[key] = 0

    def show_puzzle(self):
        x, y = [], []
        for key in self.board:
            a, b = key
            x.append(a)
            y.append(b + abs(a) * 0.5)
        plt.xlim(-2, 10)
        plt.ylim(-5, 5)
        plt.scatter(y, x, marker='s', s=[800] * len(x))
        plt.scatter([self.q[1]], [self.q[0]], marker='s', s=[800] * len(x), c='r')
        plt.show()


if __name__ == '__main__':

    p_list = [Piece(p) for p in PieceBasicData]
    puzzle = Puzzle(p_list, (-3, 1))
    puzzle.show_puzzle()

    """
    # Check shape
    
    for k in range(12):
        p = p_list[k]
        p.show(d=0)
        p.show(d=1)
        p.show(d=-1)
    """

