import shortuuid


class Piece:
    def __init__(self, name, player):
        self.name = name
        self.player = player
        self.location = None
        self.on_field = False
        self.layer = 0
        self.covered = False
        self.uuid = shortuuid.uuid()

    def __repr__(self):
        return f"{self.name}-{self.player}: {self.location}-{self.layer}\n"

    def place(self, location):
        self.on_field = True
        self.location = location

    def move(self, location, chessboard):
        if location in self.valid_location(chessboard):
            self.location = location
        else:
            raise ValueError('Illegal Movement.')

    def valid_location(self, chessboard):
        return []

