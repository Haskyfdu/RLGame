import random
import matplotlib.pyplot as plt


from HIVE.algorithms.class_Player import Player


class HIVE:
    def __init__(self):
        self.Black = Player('Black')
        self.White = Player('White')
        self.winner = None
        self.chessboard = []
        self.turn = 0

    def place(self, piece_name, location=(0, 0)):
        player = self.White if self.turn % 2 == 0 else self.Black
        queenbee = [p for p in player.pieces if p.name == 'QueenBee'][0]
        if not queenbee.on_field and self.turn >= 7 and piece_name != "QueenBee":
            raise ValueError('You have to place QueenBee in the first four turn.')
        player.place(piece_name, location, self.chessboard)
        self.turn += 1

    def move(self, piece, location):
        player = self.White if self.turn % 2 == 0 else self.Black
        queenbee = [p for p in player.pieces if p.name == 'QueenBee'][0]
        if queenbee.on_field:
            player.move(piece, location, self.chessboard)
        else:
            raise ValueError("You can't move pieces without QueenBee on field")
        self.turn += 1

    def show(self):
        self.chessboard.sort(key=lambda x: x.layer)
        for piece in self.chessboard:
            piece.show()
        plt.axis('equal')
        plt.show()

    def next_turn(self):
        player = self.White if self.turn % 2 == 0 else self.Black
        queenbee = [p for p in player.pieces if p.name == 'QueenBee'][0]
        action_pool = []
        if not queenbee.on_field and self.turn >= 6:
            place_pool = player.valid_place_location(self.chessboard)
            for location in place_pool:
                action_pool.append((queenbee, location, 'place'))
        else:
            action_pool = player.action_pool(self.chessboard)
        if len(action_pool) == 0:
            self.turn += 1
        else:
            action = random.choice(action_pool)
            if action[-1] == 'place':
                self.place(action[0].name, action[1])
            elif action[-1] == 'move':
                self.move(action[0], action[1])

    def check_win(self):
        if self.White.lose(self.chessboard):
            if self.Black.lose(self.chessboard):
                self.winner = 'Both'
            else:
                self.winner = 'Black'
        if self.Black.lose(self.chessboard):
            self.winner = 'White'

    def play(self):
        while self.winner is None:
            self.next_turn()
            self.check_win()
            print(self.turn)
            self.show()


if __name__ == '__main__':

    Game = HIVE()
    Game.play()
