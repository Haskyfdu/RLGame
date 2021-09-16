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
        self.pieces_on_field.append(piece)
        chessboard.append(piece)

    def valid_place_location(self, chessboard):
        if len(chessboard) == 0:
            return [(0, 0)]
        elif len(chessboard) == 1:
            return [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
        else:
            valid_location, location_list = [], []
            for piece in self.pieces_on_field:
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

    def action_pool(self, chessboard):
        action_pool = []
        queenbee = self.pieces[0]
        for piece in self.pieces:
            if piece.on_field:
                if queenbee.on_field:
                    move_pool = piece.valid_location(chessboard)
                    for location in move_pool:
                        action_pool.append((piece, location, 'move'))
            else:
                place_pool = self.valid_place_location(chessboard)
                for location in place_pool:
                    action_pool.append((piece, location, 'place'))
        return action_pool

    def queenbee_health(self, chessboard, opponent=None):
        opponent_queenbee, queenbee = opponent.pieces[0], self.pieces[0]
        health, opponent_health = None, None
        if queenbee.on_field:
            location_list = list(set([p.location for p in chessboard]))
            exist_neighbour = [p for p in around_location(queenbee.location) if p in location_list]
            health = 6 - len(exist_neighbour)
        else:
            health = 6
        if opponent is not None:
            if opponent_queenbee.on_field:
                location_list = list(set([p.location for p in chessboard]))
                exist_neighbour = [p for p in around_location(opponent_queenbee.location) if p in location_list]
                opponent_health = 6 - len(exist_neighbour)
            else:
                opponent_health = 6
        return health, opponent_health

    def lose(self, chessboard):
        return self.queenbee_health(chessboard)[0] == 0

    def attack_score(self, chessboard, opponent):
        score = 0
        opponent_queenbee, queenbee = opponent.pieces[0], self.pieces[0]
        location_list = around_location(opponent_queenbee.location) if opponent_queenbee.on_field else []
        for piece in self.pieces:
            if piece.on_field:
                if piece.location in location_list+[opponent_queenbee.location]:
                    pass
                elif piece.cant_move(chessboard) and piece.location not in location_list+[opponent_queenbee.location]:
                    score -= piece.attack
                elif queenbee.on_field and :
                    score += piece.attack
        return score

    def defense(self, chessboard, opponent):
        score = 0
        queenbee = self.pieces[0]
        location_list = around_location(queenbee.location) if queenbee.on_field else []
        for piece in opponent.pieces:
            if piece.on_field:
                if piece.cant_move(chessboard) and piece.location not in location_list+[queenbee.location]:
                    score += piece.attack
                else:
                    score -= piece.attack

if __name__ == '__main__':

    Hasky = Player('Hasky')
    Hattie = Player('Hattie')
