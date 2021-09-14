from HIVE.algorithms.class_Player import Player
from HIVE.algorithms.chessboard_manager import check_chessboard


class HIVE:
    def __init__(self):
        self.Black = Player('Black')
        self.White = Player('White')
        self.winner = None
        self.chessboard = []
        self.white_turn = True

    def place(self, piece_name, location=(0, 0)):
        player = self.White if self.white_turn else self.Black
        queenbee = [p for p in player.pieces if p.name == 'QueenBee'][0]
        if not queenbee.on_field and len(player.pieces_on_field) == 3 and piece_name != "QueenBee":
            raise ValueError('You have to place QueenBee in the first four turn.')
        player.place(piece_name, location, self.chessboard)
        self.white_turn = not self.white_turn

    def move(self, piece, location):
        player = self.White if self.white_turn else self.Black
        queenbee = [p for p in player.pieces if p.name == 'QueenBee'][0]
        if queenbee.on_field:
            player.move(piece, location, self.chessboard)
        else:
            raise ValueError("You can't move pieces without QueenBee on field")
        self.white_turn = not self.white_turn

    def show(self):
        print(self.chessboard)


if __name__ == '__main__':

    Game = HIVE()
    Game.place("Spider")
    Game.place("QueenBee", (0, 1))
    Game.place("Beetle", (0, -1))
    Game.place("Beetle", (1, 1))
    Game.place("QueenBee", (1, -1))
    Game.move(Game.chessboard[3], (0, 1))
    print(check_chessboard(Game.chessboard))

