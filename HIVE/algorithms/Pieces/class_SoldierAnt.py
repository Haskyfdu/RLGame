from HIVE.algorithms.Pieces.class_Piece import Piece


class SoldierAnt(Piece):
    def __init__(self, player):
        Piece.__init__(self, 'SoldierAnt', player)

    def valid_location(self, game):
        pass
