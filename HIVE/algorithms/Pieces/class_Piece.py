import shortuuid
from HIVE.algorithms.chessboard_manager import around_location, one_step, check_chessboard

class Piece:
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.location = None
        self.on_field = False
        self.layer = 0
        self.covered = False
        self.uuid = shortuuid.uuid()

    def __repr__(self):
        return f"{self.name}-{self.player}: {self.location}-{self.layer}\n"

    def place(self, location):
        self.on_field = True
        self.location = location

    def move(self, location, chessboard):
        if location in self.valid_location(chessboard):
            self.location = location
        else:
            raise ValueError('Illegal Movement.')

    def valid_location(self, chessboard):
        valid_location = []
        if self.covered:
            return valid_location
        virtual_chessboard = chessboard.copy()
        virtual_chessboard.remove(self)
        if not check_chessboard(virtual_chessboard):
            return valid_location

        location_list = list(set([p.location for p in chessboard]))
        exist_neighbour = [p for p in around_location(self.location) if p in location_list]
        for neighbour in exist_neighbour:
            valid_location.extend(one_step(self.location, neighbour, chessboard))
        # print(valid_location)
        return valid_location

