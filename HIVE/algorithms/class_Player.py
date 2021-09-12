from HIVE.algorithms.class_Piece import Piece


def distance(location1, location2):
    if location1[0] > location2[0]:
        location1, location2 = location2, location1
    dx = abs(location1[0] - location2[0])
    dy = abs(location1[1] - location2[1])
    if location2[1] >= location1[1]:
        return dx + dy
    else:
        return max(dx, dy)


def around_location(location):
    return [(location[0]+1, location[1]), (location[0]-1, location[1]),
            (location[0], location[1]+1), (location[0], location[1]-1),
            (location[0]-1, location[1]+1), (location[0]+1, location[1]-1)]


class Player:
    def __init__(self, player_id):
        self.player_id = player_id
        self.chessboard = []
        self.pieces_on_field = []
        self.hands = {'QueenBee': 1, 'Beetle': 2, 'Grasshopper': 3,
                      'Spider': 2, 'SoldierAnt': 3}

    def update_chessboard(self, other):
        self.chessboard = self.pieces_on_field + other.pieces_on_field

    def place(self, piece_name, location):
        if piece_name not in self.hands:
            raise KeyError('unknown piece name')
        elif self.hands[piece_name] == 0:
            raise ValueError("You don't have more {0}".format(piece_name))
        else:
            valid_location = self.valid_place_location()
            if location in valid_location:
                piece = Piece(piece_name, location, self.player_id)
                self.pieces_on_field.append(piece)
                self.hands[piece_name] -= 1
            else:
                raise ValueError('Illegal placement.')

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
