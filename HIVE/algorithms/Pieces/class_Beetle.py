from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import around_location, one_step, check_chessboard


class Beetle(Piece):
    def __init__(self, player):
        Piece.__init__(self, 'Beetle', player)

    def valid_location(self, chessboard):
        valid_location = Piece.valid_location(self, chessboard)
        location_list = list(set([p.location for p in chessboard]))
        exist_neighbour = [p for p in around_location(self.location) if p in location_list]
        valid_location.extend(exist_neighbour)
        return valid_location

    def move(self, location, chessboard):
        covered_pieces = [p for p in chessboard if p.location == location]
        for piece in covered_pieces:
            piece.covered = True
        old_location = self.location
        Piece.move(self, location, chessboard)
        self.layer = len(covered_pieces)
        uncovered_pieces = [p for p in chessboard if p.location == old_location]
        uncovered_pieces.sort(key=lambda x: x.layer)
        if len(uncovered_pieces) > 0:
            uncovered_pieces[-1].covered = False



