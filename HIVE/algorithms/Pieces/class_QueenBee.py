from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import one_step, check_chessboard, check_occupy


class QueenBee(Piece):
    def __init__(self, player):
        Piece.__init__(self, 'QueenBee', player)

    def valid_location(self, chessboard):
        valid_location = []
        if self.covered:
            return valid_location
        virtual_chessboard = chessboard.copy()
        virtual_chessboard.remove(self)
        if not check_chessboard(virtual_chessboard):
            return valid_location




