from HIVE.algorithms.Pieces.class_Piece import Piece


class Grasshopper(Piece):
    def __init__(self, player):
        super().__init__('Grasshopper', player)

    def valid_location(self, chessboard):
        valid_location = []
        if super().cant_move(chessboard):
            return valid_location
        chart = [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
        for direction in chart:
            pass
        return []


