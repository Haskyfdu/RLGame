from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import around_location, one_step, check_chessboard


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

        location_list = list(set([p.location for p in chessboard]))
        exist_neighbour = [p for p in around_location(self.location) if p in location_list]
        for neighbour in exist_neighbour:
            valid_location.extend(one_step(self.location, neighbour, chessboard))
        # print(valid_location)
        return valid_location





