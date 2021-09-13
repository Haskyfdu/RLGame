from HIVE.algorithms.Pieces.class_QueenBee import QueenBee
from HIVE.algorithms.Pieces.class_Beetle import Beetle
from HIVE.algorithms.Pieces.class_Grasshopper import Grasshopper
from HIVE.algorithms.Pieces.class_Spider import Spider
from HIVE.algorithms.Pieces.class_SoldierAnt import SoldierAnt


class Player:
    def __init__(self, player):
        self.player = player
        self.pieces_on_field = []
        self.hands = self.set_hands()

    def set_hands(self):
        hands = [QueenBee(self.player),
                 Beetle(self.player), Beetle(self.player),
                 Grasshopper(self.player), Grasshopper(self.player), Grasshopper(self.player),
                 Spider(self.player), Spider(self.player),
                 SoldierAnt(self.player), SoldierAnt(self.player), SoldierAnt(self.player)]
        return hands

    def place(self, piece_name, location):
        available_piece = [p for p in self.hands if p.name == piece_name and not p.on_field]
        if len(available_piece) == 0:
            raise KeyError(f'No {piece_name} is available')
        else:
            piece = available_piece[0]
        valid_location = self.valid_place_location()
        if location in valid_location:
            piece.place(location)
        else:
            raise ValueError(f'Illegal placement {location}.')

    def valid_place_location(self):
        if len(self.pieces_on_field) == 0:
            if len(self.chessboard) == 0:
                return [(0, 0)]
            elif len(self.chessboard) == 1:
                return [(0, 1)]
        else:
            valid_location = []
            location_list = []
            for piece in self.pieces_on_field:
                location_list.extend(around_location(piece.location))
            location_list = list(set(location_list))
            others = [p for p in self.chessboard if p.player != self.player_id]
            for location in location_list:
                for piece in others:
                    d = distance(piece.location, location)
                    if d <= 1:
                        break
                else:
                    valid_location.append(location)
            valid_location = list(set(valid_location)-set([p.location for p in self.pieces_on_field]))
            return valid_location


if __name__ == '__main__':

    Hasky = Player('Hasky')
    Hattie = Player('Hattie')
    print(Hasky.hands)
    print(Hattie.hands)
    Hasky.place('Beetle', (0, 0))
    Hattie.update_chessboard(Hasky)
    Hattie.place('QueenBee', (0, 1))
    Hasky.update_chessboard(Hattie)
    Hasky.place('QueenBee', (-1, 0))
    Hattie.update_chessboard(Hasky)

    print(Hasky.chessboard)
    print(Hattie.chessboard)
    print(Hasky.hands)
    print(Hattie.hands)
