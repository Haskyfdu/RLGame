from HIVE.algorithms.class_action import Action
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

    def play(self, action, chessboard):
        if action.action_type == 'place':
            self.place(action.piece, action.target_location, chessboard)
        elif action.action_type == 'move':
            self.move(action.piece, action.target_location, chessboard)
        self.turn += 1

    def place(self, piece, target_location, chessboard):
        valid_location = self.get_valid_place_location(chessboard)
        if target_location in valid_location:
            piece.place(target_location)
        else:
            raise ValueError(f'Illegal placement {target_location}.')
        self.pieces_on_field.append(piece)
        chessboard.append(piece)

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

    def move(self, piece, target_location, chessboard):
        if piece.player != self.player:
            raise ValueError(f"You can only move your pieces.")
        piece.move(target_location, chessboard)

    def enumerate_action_pool(self, chessboard):
        action_pool = []
        place_location_pool = self.get_valid_place_location(chessboard)
        if not self.queenbee.on_field and self.turn >= 3:
            for location in place_location_pool:
                action_pool.append(Action(self.queenbee, location, 'place'))
                return action_pool
        else:
            for piece in self.pieces:
                if piece.on_field:
                    if self.queenbee.on_field:
                        move_pool = piece.valid_target_location(chessboard)
                        for location in move_pool:
                            action_pool.append(Action(piece, location, 'move'))
                else:
                    for location in place_location_pool:
                        action_pool.append(Action(piece, location, 'place'))
            return action_pool

    def queenbee_health(self, chessboard):
        if self.queenbee.on_field:
            location_list = list(set([p.location for p in chessboard]))
            exist_neighbour = [p for p in get_neighbours(self.queenbee.location) if p in location_list]
            health = 6 - len(exist_neighbour)
        else:
            health = 6
        return health

    def lose(self, chessboard):
        return self.queenbee_health(chessboard) == 0

    def score(self, chessboard, opponent):
        health = self.queenbee_health(chessboard)
        opponent_health = opponent.queenbee_health(chessboard)
        score = 100 * (6 - opponent_health)
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
            old_location = action.piece.location
            self.play(action, chessboard)
            score = self.score(chessboard, opponent)
            self.undo(action, old_location)
            print(chessboard, action, score)
            if score > best_score:
                best_action = action
        return best_action


if __name__ == '__main__':

    Hasky = Player('Hasky')
    Hattie = Player('Hattie')
