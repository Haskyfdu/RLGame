class Action:
    def __init__(self, piece, target_location, action_type):
        self.piece = piece
        self.target_location = target_location
        self.action_type = action_type
        self.score = None
