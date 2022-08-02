from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import check_occupy, Chart


class Grasshopper(Piece):
    def __init__(self, player):
        super().__init__('Grasshopper', player)
        self.attack = 30

    def valid_location(self, chessboard):
        valid_location = []
        if super().cant_move(chessboard):
            return valid_location
        for direction in Chart:
            location = (self.location[0]+direction[0], self.location[1]+direction[1])
            d = 0
            while check_occupy(location, chessboard):
                d += 1
                location = (location[0]+direction[0], location[1]+direction[1])
            if d >= 1:
                valid_location.append(location)
        return list(set(valid_location))

    def show(self, piece_color='green'):
        super().show(piece_color)
