from HIVE.algorithms.Pieces.class_Piece import Piece


class Grasshopper(Piece):
    def __init__(self, player):
        Piece.__init__(self, 'Grasshopper', player)

    def valid_location(self, game):
        pass
