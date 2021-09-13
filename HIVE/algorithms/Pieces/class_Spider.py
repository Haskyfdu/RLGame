from HIVE.algorithms.Pieces.class_Piece import Piece


class Spider(Piece):
    def __init__(self, player):
        Piece.__init__(self, 'Spider', player)

    def valid_location(self, game):
        pass
