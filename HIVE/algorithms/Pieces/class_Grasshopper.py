from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import check_occupy


class Grasshopper(Piece):
    def __init__(self, player):
        super().__init__('Grasshopper', player)

    def valid_location(self, chessboard):
        valid_location = []
        if super().cant_move(chessboard):
            return valid_location
        chart = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
        for direction in chart:
            location = (self.location[0]+direction[0], self.location[1]+direction[1])
            while check_occupy(location, chessboard):
                location = (location[0]+direction[0], location[1]+direction[1])
            valid_location.append(location)
        return []
