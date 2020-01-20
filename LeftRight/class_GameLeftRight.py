import copy
import random
import matplotlib.pyplot as plt


Alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class GameLeftRight:
    def __init__(self, mu, sigma, num_learning_rounds, run_times):
        self.run_times = run_times
        self.num_learning_rounds = num_learning_rounds
        self.left_times = 0
        self.right_times = 0
        self.mu = mu
        self.sigma = sigma
        self.last_state = None
        self.last_action = None
        self.state = None
        self.action = None
        self.reward = None
        self.gamma = 1
        self.epsilon = 0.1
        self.learning_rate = 0.1
        self.Q = {'A': {'left': 0.0, 'right': 0.0},
                  'B': {Alphabet[p]: 0.0 for p in range(26)},
                  'end': 0.0}
        self.QQ1 = copy.deepcopy(self.Q)
        self.QQ2 = copy.deepcopy(self.Q)

    def restart(self):
        self.left_times = 0
        self.right_times = 0
        self.Q = {'A': {'left': 0.0, 'right': 0.0},
                  'B': {Alphabet[p]: 0.0 for p in range(26)},
                  'end': 0.0}
        self.QQ1 = copy.deepcopy(self.Q)
        self.QQ2 = copy.deepcopy(self.Q)

    def reset(self):
        self.state = 'A'

    def get_action(self):
        if self.state == 'B':
            if random.random() > self.epsilon:
                max_q = -99
                for p in Alphabet:
                    if self.Q[self.state][p] > max_q:
                        self.action = p
                        max_q = self.Q[self.state][p]
            else:
                self.action = Alphabet[random.randint(0, 25)]
        elif self.state == 'A':
            if random.random() > self.epsilon:
                if self.Q['A']['left'] > self.Q['A']['right']:
                    self.action = 'left'
                elif self.Q['A']['left'] == self.Q['A']['right']:
                    self.action = random.choice(['right', 'left'])
                else:
                    self.action = 'right'
            else:
                self.action = random.choice(['right', 'left'])
        else:
            raise ValueError

    def get_action_QQ(self):
        if self.state == 'B':
            if random.random() > self.epsilon:
                max_q = -99
                for p in Alphabet:
                    if self.QQ1[self.state][p] + self.QQ2[self.state][p] > max_q:
                        self.action = p
                        max_q = self.QQ1[self.state][p] + self.QQ2[self.state][p]
            else:
                self.action = Alphabet[random.randint(0, 25)]
        elif self.state == 'A':
            if random.random() > self.epsilon:
                if self.QQ1['A']['left']+self.QQ2['A']['left'] \
                        > self.QQ1['A']['right']+self.QQ2['A']['right']:
                    self.action = 'left'
                elif self.QQ1['A']['left']+self.QQ2['A']['left'] \
                        == self.QQ1['A']['right']+self.QQ2['A']['right']:
                    self.action = random.choice(['right', 'left'])
                else:
                    self.action = 'right'
            else:
                self.action = random.choice(['right', 'left'])
        else:
            raise ValueError

    def move(self):
        if self.state == 'A':
            if self.action == 'right':
                self.last_state, self.last_action = 'A', 'right'
                self.state = 'end'
                self.reward = 0
                self.right_times += 1
            elif self.action == 'left':
                self.last_state, self.last_action = 'A', 'left'
                self.state = 'B'
                self.reward = 0
                self.left_times += 1
            else:
                raise ValueError
        elif self.state == 'B':
            if self.action in Alphabet:
                self.last_state, self.last_action = 'B', self.action
                self.state = 'end'
                self.reward = random.gauss(self.mu, self.sigma)
            else:
                raise ValueError
        else:
            raise ValueError

    def update(self):
        if self.state == 'end':
            new = self.Q['end']
        elif self.state == 'B':
            new = max([self.Q['B'][p] for p in Alphabet])
        else:
            raise ValueError
        self.Q[self.last_state][self.last_action] = \
            (1-self.learning_rate)*self.Q[self.last_state][self.last_action] + \
            self.learning_rate*(self.reward+self.gamma*new)

    def update_QQ(self):
        if self.state == 'end':
            new_qq1 = self.QQ1['end']
            new_qq2 = self.QQ2['end']
        elif self.state == 'B':
            max_q1 = -99
            max_q2 = -99
            action_q1 = 'A'
            action_q2 = 'A'
            for p in Alphabet:
                if self.QQ1['B'][p] > max_q1:
                    action_q1 = p
                    max_q1 = self.QQ1['B'][p]
                if self.QQ2['B'][p] > max_q2:
                    action_q2 = p
                    max_q2 = self.QQ2['B'][p]
            new_qq1 = self.QQ2[self.state][action_q1]
            new_qq2 = self.QQ1[self.state][action_q2]
        else:
            raise ValueError
        if random.random() > 0.5:
            self.QQ1[self.last_state][self.last_action] = \
                (1 - self.learning_rate) * self.QQ1[self.last_state][self.last_action] + \
                self.learning_rate * (self.reward + self.gamma * new_qq1)
        else:
            self.QQ2[self.last_state][self.last_action] = \
                (1 - self.learning_rate) * self.QQ2[self.last_state][self.last_action] + \
                self.learning_rate * (self.reward + self.gamma * new_qq2)

    def run(self):
        self.reset()
        while self.state != 'end':
            self.get_action()
            self.move()
            self.update()

    def run_QQ(self):
        self.reset()
        while self.state != 'end':
            self.get_action_QQ()
            self.move()
            self.update_QQ()

    def learning(self):
        left_percent_mean = [0.0] * self.num_learning_rounds
        left_percent_mean_qq = [0.0] * self.num_learning_rounds
        for j in range(self.run_times):
            self.restart()
            for i in range(self.num_learning_rounds):
                self.run()
                left_percent_mean[i] += self.left_times/(self.left_times+self.right_times)
            self.restart()
            for i in range(self.num_learning_rounds):
                self.run_QQ()
                left_percent_mean_qq[i] += self.left_times/(self.left_times+self.right_times)
        left_percent_mean = [left_percent_mean[i]/self.run_times for i in range(self.num_learning_rounds)]
        left_percent_mean_qq = [left_percent_mean_qq[i] / self.run_times for i in range(self.num_learning_rounds)]
        plt.plot(range(self.num_learning_rounds), left_percent_mean)
        plt.plot(range(self.num_learning_rounds), left_percent_mean_qq)
        plt.show()


if __name__ == '__main__':

    Game = GameLeftRight(mu=-0.1, sigma=1.0, num_learning_rounds=5000, run_times=1000)
    Game.learning()
