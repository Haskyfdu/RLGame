import shortuuid
import numpy as np
import matplotlib.pyplot as plt


from HIVE.algorithms.chessboard_manager import around_location, one_step, check_chessboard


class Piece:
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.location = None
        self.on_field = False
        self.layer = 0
        self.covered = False
        self.attack = 0
        self.uuid = shortuuid.uuid()

    def __repr__(self):
        return f"{self.name}-{self.player}: {self.location}-{self.layer}"

    def place(self, location):
        self.on_field = True
        self.location = location

    def move(self, location, chessboard):
        if location in self.valid_location(chessboard):
            self.location = location
        else:
            raise ValueError('Illegal Movement.')

    def cant_move(self, chessboard):
        if self.covered:
            return True
        virtual_chessboard = chessboard.copy()
        virtual_chessboard.remove(self)
        if not check_chessboard(virtual_chessboard):
            return True
        return False

    def valid_location(self, chessboard):
        valid_location = []
        if self.cant_move(chessboard):
            return valid_location
        exist_neighbour = [p for p in chessboard if p.location in around_location(self.location)
                           and p.layer == self.layer]
        for neighbour in exist_neighbour:
            valid_location.extend(one_step(self.location, neighbour.location, chessboard))
        # print(valid_location)
        return list(set(valid_location))

    def show(self, piece_color):
        center = ((self.location[0]*2+self.location[1])*np.cos(np.pi/6)+self.layer*0.05,
                  self.location[1]*(1+np.sin(np.pi/6))+self.layer*0.05)
        theta = np.linspace(0, 2 * np.pi, 7) + np.pi / 2
        x = np.cos(theta) + center[0]
        y = np.sin(theta) + center[1]
        fill_color = 'k' if self.player == 'Black' else 'Bisque'
        plt.plot(x, y, color='w')
        plt.fill(x, y, fill_color)
        x = 0.3*np.cos(theta) + center[0]
        y = 0.3*np.sin(theta) + center[1]
        plt.plot(x, y, color=piece_color)
        plt.fill(x, y, piece_color)

    def copy(self):
        piece = Piece(self.name, self.player)
        piece.__dict__.update(self.__dict__)
        return piece
