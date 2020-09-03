from Tokaido.Traveler import OldMan, Priest, StreetEntertainer


class Tokaido:
    def __init__(self):
        self.player1 = OldMan()
        self.player2 = Priest()
        self.player3 = StreetEntertainer()
        self.len = 30
        self.round = 0
        self.state = None
        self.get_state()
        self.is_terminal = False
        self.reward = None

    def reset(self):
        self.player1 = OldMan()
        self.player2 = Priest()
        self.player3 = StreetEntertainer()
        self.round = 0
        self.is_terminal = False

    def get_state(self):
        self.state = {'location': [self.player1.location, self.player2.location, self.player3.location],
                      'coins': [self.player1.coins, self.player2.coins, self.player3.coins],
                      'score': [self.player1.score, self.player2.score, self.player3.score],
                      'sea': [self.player1.sea, self.player2.sea, self.player3.sea],
                      'mountain': [self.player1.mountain, self.player2.mountain, self.player3.mountain],
                      'paddy': [self.player1.paddy, self.player2.paddy, self.player3.paddy],
                      'hot_spring': [self.player1.hot_spring, self.player2.hot_spring, self.player3.hot_spring],
                      'donated': [self.player1.donated, self.player2.donated, self.player3.donated]}

    def one_move(self, action):
        pass

    def get_action(self):
        pass
