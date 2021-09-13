from HIVE.algorithms.Pieces.class_QueenBee import QueenBee
from HIVE.algorithms.Pieces.class_Beetle import Beetle
from HIVE.algorithms.Pieces.class_Grasshopper import Grasshopper
from HIVE.algorithms.Pieces.class_Spider import Spider
from HIVE.algorithms.Pieces.class_SoldierAnt import SoldierAnt
from HIVE.algorithms.chessboard_manager import around_location, distance


class Player:
    def __init__(self, player):
        self.player = player
        self.pieces_on_field = []
        self.pieces = self.set_pieces()

    def set_pieces(self):
        pieces = [QueenBee(self.player),
                  Beetle(self.player), Beetle(self.player),
                  Grasshopper(self.player), Grasshopper(self.player), Grasshopper(self.player),
                  Spider(self.player), Spider(self.player),
                  SoldierAnt(self.player), SoldierAnt(self.player), SoldierAnt(self.player)]
        return pieces

    def place(self, piece_name, location, chessboard):
        available_piece = [p for p in self.pieces if p.name == piece_name and not p.on_field]
        if len(available_piece) == 0:
            raise KeyError(f'No {piece_name} is available')
        else:
            piece = available_piece[0]
        valid_location = self.valid_place_location(chessboard)
        if location in valid_location:
            piece.place(location)
        else:
            raise ValueError(f'Illegal placement {location}.')
        chessboard.append(piece)

    def valid_place_location(self, chessboard):
        if len(chessboard) == 0:
            return [(0, 0)]
        elif len(chessboard) == 1:
            return [(0, 1)]
        else:
            valid_location, location_list = [], []
            for piece in self.pieces:
                if piece.on_field:
                    location_list.extend(around_location(piece.location))
            location_list = list(set(location_list))
            opponent_pieces = [p for p in chessboard if p.player != self.player and not p.covered]
            for location in location_list:
                for piece in opponent_pieces:
                    d = distance(piece.location, location)
                    if d <= 1:
                        break
                else:
                    valid_location.append(location)
            valid_location = list(set(valid_location)-set([p.location for p in self.pieces_on_field]))
            return valid_location

    def move(self, piece, location, chessboard):
        if piece.player != self.player:
            raise ValueError(f"You can only move your pieces.")
        piece.move(location, chessboard)


if __name__ == '__main__':

    Hasky = Player('Hasky')
    Hattie = Player('Hattie')
