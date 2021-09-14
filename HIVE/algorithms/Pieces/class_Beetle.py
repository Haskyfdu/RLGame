from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import around_location, right_left_door, Chart


class Beetle(Piece):
    def __init__(self, player):
        super().__init__('Beetle', player)

    def valid_location(self, chessboard):
        valid_location = []
        if self.cant_move(chessboard):
            return valid_location
        if self.layer >= 2:
            return around_location(self.location)
        elif self.layer == 1:
            for move_location in around_location(self.location):
                right_door_layer, left_door_layer = self.right_left_doors_layer(move_location, chessboard)
                move_location_layer = len([p for p in chessboard if p.location == move_location])
                if right_door_layer >= 2 > move_location_layer and left_door_layer >= 2:
                    continue
                else:
                    valid_location.append(move_location)
            return valid_location
        elif self.layer == 0:
            valid_location = super().valid_location(chessboard)
            for move_location in around_location(self.location):
                right_door_layer, left_door_layer = self.right_left_doors_layer(move_location, chessboard)
                move_location_layer = len([p for p in chessboard if p.location == move_location])
                if move_location_layer == 0:
                    continue
                elif move_location_layer == 1:
                    if right_door_layer >= 2 and left_door_layer >= 2:
                        continue
                    else:
                        valid_location.append(move_location)
                else:
                    valid_location.append(move_location)
            return list(set(valid_location))
        else:
            raise ValueError('Beetle Layer Bug!')

    def right_left_doors_layer(self, move_location, chessboard):
        relative_position = (move_location[0] - self.location[0], move_location[1] - self.location[1])
        i, j = right_left_door(relative_position)
        right_door = (self.location[0] + Chart[i][0], self.location[1] + Chart[i][1])
        left_door = (self.location[0] + Chart[j][0], self.location[1] + Chart[j][1])
        right_door_layer = len([p for p in chessboard if p.location == right_door])
        left_door_layer = len([p for p in chessboard if p.location == left_door])
        return right_door_layer, left_door_layer

    def move(self, location, chessboard):
        covered_pieces = [p for p in chessboard if p.location == location]
        for piece in covered_pieces:
            piece.covered = True
        old_location = self.location
        super().move(location, chessboard)
        self.layer = len(covered_pieces)
        uncovered_pieces = [p for p in chessboard if p.location == old_location]
        if len(uncovered_pieces) > 0:
            uncovered_pieces.sort(key=lambda x: x.layer)
            uncovered_pieces[-1].covered = False



