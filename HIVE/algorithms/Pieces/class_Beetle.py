from HIVE.algorithms.Pieces.class_Piece import Piece


class Beetle(Piece):
    def __init__(self, player):
        Piece.__init__(self, 'Beetle', player)

    def valid_location(self, game):
        pass
