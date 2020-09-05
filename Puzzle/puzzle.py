from matplotlib import pyplot as plt
from typing import List
from copy import deepcopy

Scatter_markers = ['s', 'o', '^', '8', 'p', 'd', 'v', 'h', '>', '<']
Scatter_colors = ['c', 'b', 'g', 'm',
                  'y', 'k', 'peru', 'plum',
                  'teal', 'darkred', 'lightgrey', 'cyan']

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
        self.shape = [(0, 0)] + shape_list
        self.location = (0, 0)
        self.new_shape = None
        self.d = 0

    def spin(self, d=0):
        new_shape = []
        for p in self.shape:
            a, b = 0, 0
            if d == 0:
                a = p[0]
                b = p[1]
            elif d == 1:
                self.d = 1
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
                self.d = -1
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
            new_shape.append((a, b))
        self.new_shape = new_shape

    def move(self, step=(0, 0)):
        self.location = step
        new_shape = []
        for p in self.new_shape:
            a, b = p
            if step[0]*a < 0:
                b += min(abs(step[0]), abs(a))
            a += step[0]
            b += step[1]
            new_shape.append((a, b))
        self.new_shape = new_shape

    # def move2(self, step=(0, 0)):
    #     temp_shape, new_shape = [], []
    #     for p in self.new_shape:
    #         if p[0] < 0:
    #             temp_shape.append((p[0]+step[0], p[1]-p[0]+step[1]))
    #         else:
    #             temp_shape.append((p[0]+step[0], p[1]+step[1]))
    #     for p in temp_shape:
    #         if p[0] < 0:
    #             new_shape.append((p[0], p[1]+p[0]))
    #         else:
    #             new_shape.append(p)
    #     self.new_shape = new_shape

    def show(self, step=(0, 0), d=0):
        x, y = [], []
        self.spin(d)
        self.move(step)
        for key in self.new_shape:
            a, b = key
            x.append(a)
            y.append(b + abs(a) * 0.5)
        plt.xlim(-2, 10)
        plt.ylim(-5, 5)
        plt.scatter(y, x, marker='s', s=[800]*len(x))
        plt.show()

    def check(self):
        for p in self.new_shape:
            if -4 <= p[0] <= 4 and 0 <= p[1] <= 8-abs(p[0]):
                continue
            else:
                return False
        return True

    def reset(self):
        self.new_shape = self.shape


class Puzzle:
    def __init__(self, piece_list: List[Piece], q=(0, 4)):
        self.board = {}
        self.build_board()
        self.q = q
        self.board[q] = 1
        self.piece_list = piece_list
        self.puzzle_status = None
        self.steps = None
        self.next_key = None
        self.status_list = None

    def build_board(self):
        for i in range(-4, 5):
            for j in range(9 - abs(i)):
                key = (i, j)
                self.board[key] = 0

    def matching(self):
        plan_list = []
        for i in range(12):
            used_pieces = [p['id'] for p in self.steps]
            if i not in used_pieces:
                piece = self.piece_list[i]
                for d in [0, 1, -1]:
                    piece.spin(d)
                    key_list = piece.new_shape.copy()
                    for key in key_list:
                        ppp = self.next_key[0] - key[0]
                        if ppp*key[0] < 0:
                            step = (self.next_key[0] - key[0],
                                    self.next_key[1] - key[1] - min(abs(ppp), abs(key[0])))
                        else:
                            step = (self.next_key[0]-key[0], self.next_key[1]-key[1])
                        piece.move(step)

                        # if key[0] < 0:
                        #     a = (key[0], key[1]-key[0])
                        # else:
                        #     a = key
                        # if self.next_key[0] < 0:
                        #     dis = (self.next_key[0], self.next_key[1] - self.next_key[0])
                        # else:
                        #     dis = self.next_key
                        # move = (dis[0]-a[0], dis[1]-a[1])
                        # piece.move2(move)

                        if piece.check():
                            if sum([self.puzzle_status[key2] for key2 in piece.new_shape]) == 0:
                                plan = {'position': step, 'id': i, 'd': d}
                                plan_list.append(plan)
                        piece.reset()
                        piece.spin(d)
        return plan_list

    def positioning(self):
        for i in range(-4, 5):
            for j in range(9 - abs(i)):
                key = (i, j)
                if self.puzzle_status[key] == 0:
                    return key
        return None

    def action(self, plan):
        piece = self.piece_list[plan['id']]
        piece.spin(plan['d'])
        piece.move(plan['position'])
        for key in piece.new_shape:
            self.puzzle_status[key] = plan['id']+1

    def solve(self):
        puzzle_status = self.board.copy()
        self.status_list = {0: [{'steps': [{'position': self.q, 'id': -1, 'd': 0}],
                                 'puzzle_status': puzzle_status}]}
        for i in range(13):
            self.status_list[i+1] = []
            # print(i, len(self.status_list[i]))
            for status in self.status_list[i]:
                self.puzzle_status = deepcopy(status['puzzle_status'])
                self.steps = status['steps']

                self.next_key = self.positioning()
                plan_list = self.matching()
                if len(plan_list) > 0:
                    for plan in plan_list:
                        self.action(plan)
                        # self.show_ans(self.puzzle_status)
                        puzzle_status = deepcopy(self.puzzle_status)
                        self.status_list[i+1].append({'steps': self.steps+[plan],
                                                      'puzzle_status': puzzle_status})
                        self.puzzle_status = deepcopy(status['puzzle_status'])

    def show_ans(self, puzzle_status, filename):
        x, y, z = [], [], []
        plt.xlim(-2, 10)
        plt.ylim(-5, 5)
        for key in puzzle_status:
            if puzzle_status[key] > 0:
                a, b = key
                z.append(Scatter_colors[puzzle_status[key]-1])
                x.append(a)
                y.append(b + abs(a) * 0.5)
        plt.scatter(y, x, marker='s', s=800, c=z)
        plt.scatter([self.q[1] + abs(self.q[0]) * 0.5], [self.q[0]],
                    marker='s', s=[800] * len(x), c='r')
        plt.savefig(filename)
        plt.show()


if __name__ == '__main__':

    for u in range(-4, 5):
        for v in range(9 - abs(u)):
            problem = (u, v)

            p_list = [Piece(p) for p in PieceBasicData]
            puzzle = Puzzle(p_list, problem)
            puzzle.solve()
            print(problem, len(puzzle.status_list[12]))
            if len(puzzle.status_list[12]) > 0:
                png_name = str(problem[0])+','+str(problem[1])+'-ans.png'
                puzzle.show_ans(puzzle.puzzle_status, png_name)


