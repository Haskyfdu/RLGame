from HIVE.algorithms.Pieces.class_Piece import Piece


class SoldierAnt(Piece):
    def __init__(self, player):
        super().__init__('SoldierAnt', player)

    def valid_location(self, chessboard):
        valid_location = []
        if super().cant_move(chessboard):
            return valid_location
        
