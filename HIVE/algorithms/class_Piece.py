import shortuuid


class Piece:
    def __init__(self, name, location, player):
        self.name = name
        self.location = location
        self.player = player
        self.uuid = shortuuid.uuid()

    def move(self):
        pass

    def jump(self):
        pass

    def __repr__(self):
        return "{0}-{1}: {2}\n".format(self.name, self.player, self.location)

    def to_json(self):
        return {'name': self.name, 'location': self.location,
                'player': self.player, 'uuid': self.uuid}

