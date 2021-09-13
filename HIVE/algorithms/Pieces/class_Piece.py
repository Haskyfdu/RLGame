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
        return "{0}-{1}: {2}\n".format(self.name, self.player, self.location)

    def place(self, location):
        self.on_field = True
        self.location = location

    def move(self, location):
        self.location = location

