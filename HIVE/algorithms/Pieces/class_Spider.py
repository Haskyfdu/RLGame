from HIVE.algorithms.Pieces.class_Piece import Piece
from HIVE.algorithms.chessboard_manager import basic_one_step, get_neighbours


class Spider(Piece):
    def __init__(self, player):
        super().__init__('Spider', player)
        self.attack = 20

    def valid_target_location(self, chessboard):
        route_list = [[self.location, p] for p in super().valid_target_location(chessboard)]
        if len(route_list) == 0:
            return []
        route_dict = {0: route_list, 1: [], 2: []}
        virtual_chessboard = chessboard.copy()
        virtual_chessboard.remove(self)
        for step in range(2):
            for route in route_dict[step]:
                current_location = route[-1]
                exist_neighbour = [p for p in virtual_chessboard if p.location in get_neighbours(current_location)
                                   and p.layer == self.layer]
                for neighbour in exist_neighbour:
                    next_step = basic_one_step(current_location, neighbour.location, virtual_chessboard)
                    for location in next_step:
                        if location in route:
                            continue
                        else:
                            route_dict[step+1].append(route+[location])
        valid_location = [p[-1] for p in route_dict[2]]
        # print(route_dict[2])
        return list(set(valid_location))

    def show(self, piece_color='darkgoldenrod'):
        super().show(piece_color)

