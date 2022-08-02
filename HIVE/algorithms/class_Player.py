from HIVE.algorithms.Pieces.class_Beetle import Beetle
from HIVE.algorithms.Pieces.class_Spider import Spider
from HIVE.algorithms.Pieces.class_QueenBee import QueenBee
from HIVE.algorithms.Pieces.class_SoldierAnt import SoldierAnt
from HIVE.algorithms.Pieces.class_Grasshopper import Grasshopper
from HIVE.algorithms.chessboard_manager import get_neighbours, distance


class Player:
    def __init__(self, player):
        self.player = player
        self.pieces_on_field = []
        self.pieces = self.set_pieces()
        self.queenbee = self.pieces[0]
        self.turn = 0

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
        valid_location = self.get_valid_place_location(chessboard)
        if location in valid_location:
            piece.place(location)
        else:
            raise ValueError(f'Illegal placement {location}.')
        self.pieces_on_field.append(piece)
        chessboard.append(piece)
        self.turn += 1

    def get_valid_place_location(self, chessboard):
        if len(chessboard) == 0:
            return [(0, 0)]
        elif len(chessboard) == 1:
            return [(0, 1), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1)]
        else:
            valid_location, location_list = [], []
            for piece in self.pieces_on_field:
                location_list.extend(get_neighbours(piece.location))
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
                place_pool = self.get_valid_place_location(chessboard)
                for location in place_pool:
                    action_pool.append((piece, location, 'place'))
        return action_pool

    def queenbee_health(self, chessboard, opponent=None):
        queenbee = self.pieces[0]
        health, opponent_health = None, None
        if queenbee.on_field:
            location_list = list(set([p.location for p in chessboard]))
            exist_neighbour = [p for p in get_neighbours(queenbee.location) if p in location_list]
            health = 6 - len(exist_neighbour)
        else:
            health = 6
        if opponent is not None:
            opponent_queenbee = opponent.pieces[0]
            if opponent_queenbee.on_field:
                location_list = list(set([p.location for p in chessboard]))
                exist_neighbour = [p for p in get_neighbours(opponent_queenbee.location) if p in location_list]
                opponent_health = 6 - len(exist_neighbour)
            else:
                opponent_health = 6
        return health, opponent_health

    def lose(self, chessboard):
        return self.queenbee_health(chessboard)[0] == 0

    def score(self, chessboard, opponent):
        health, opponent_health = self.queenbee_health(chessboard, opponent)
        score = 100 * (health - opponent_health)
        queenbee = self.pieces[0]
        opponent_queenbee = opponent.pieces[0]
        if opponent_queenbee.on_field and opponent_queenbee.cant_move(chessboard):
            score += 200
        if queenbee.on_field:
            score += 500
            if queenbee.cant_move(chessboard):
                score -= 100
        for piece in self.pieces:
            if piece.on_field:
                if opponent_queenbee.on_field:
                    attack_range = set(piece.valid_location(chessboard))
                    target = set(get_neighbours(opponent_queenbee.location) + [opponent_queenbee.location])
                    if not attack_range.isdisjoint(target):
                        score += piece.attack
                else:
                    score -= 0.5 * piece.attack
            else:
                score += 0 * piece.attack
        for piece in opponent.pieces:
            if piece.on_field:
                if queenbee.on_field:
                    attack_range = set(piece.valid_location(chessboard))
                    target = set(get_neighbours(queenbee.location) + [queenbee.location])
                    if not attack_range.isdisjoint(target):
                        score -= piece.attack
                else:
                    score += 0.5 * piece.attack
            else:
                score -= 0 * piece.attack
        return score

    @staticmethod
    def undo(chessboard, action, old_location=None):
        if action[-1] == 'place':
            piece = chessboard.pop()
            piece.on_field = False
            piece.location = None
        elif action[-1] == 'move':
            piece = action[0]
            piece.move(old_location, chessboard)

    def best_action(self, chessboard, opponent, action_pool):
        best_score, best_action = -999999, None
        for action in action_pool:
            self.move(action[0], action[1], chessboard)
            score = self.score(virtual_chessboard, opponent)
            print(chessboard, action, score)
            if score > best_score:
                best_action = action
        return best_action


if __name__ == '__main__':

    Hasky = Player('Hasky')
    Hattie = Player('Hattie')
