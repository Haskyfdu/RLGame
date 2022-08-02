from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import get_neighbours, basic_one_step


class SoldierAnt(Piece):
    def __init__(self, player):
        super().__init__('SoldierAnt', player)
        self.attack = 50

    def valid_target_location(self, chessboard):
        if len(super().valid_target_location(chessboard)) == 0:
            return []
        valid_location = []
        start_location, current_location = self.location, self.location
        exist_neighbour = [p for p in chessboard if p.location in get_neighbours(current_location)
                           and p.layer == self.layer]
        current_neighbour = exist_neighbour[0]
        virtual_chessboard = chessboard.copy()
        virtual_chessboard.remove(self)
        while True:
            # print(current_location)
            next_step = basic_one_step(current_location, current_neighbour.location, virtual_chessboard, 'clockwise')
            if len(next_step) == 1:
                valid_location.extend(next_step)
                current_location = next_step[0]
            else:
                exist_neighbour = [p for p in virtual_chessboard if p.location in get_neighbours(current_location)
                                   and p.layer == self.layer]
                for neighbour in exist_neighbour:
                    next_step = basic_one_step(current_location, neighbour.location, virtual_chessboard, 'clockwise')
                    if len(next_step) == 1:
                        valid_location.extend(next_step)
                        current_location = next_step[0]
                        current_neighbour = neighbour
                        break
                else:
                    raise ValueError('Ant Move Bug.')
            if current_location == start_location:
                valid_location.pop()
                break
        # print(valid_location)
        return valid_location

    def show(self, piece_color='blue'):
        super().show(piece_color)


