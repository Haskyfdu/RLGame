from BlackJack.qlearner import Learner
from BlackJack.class_BlackJack import BlackJack


def main():
    num_learning_rounds = 100000
    game = BlackJack(num_learning_rounds=num_learning_rounds,
                     learner=Learner(num_learning_rounds))  # Q learner
    for k in range(0, num_learning_rounds):
        game.run()

    df = game.player.get_optimal_strategy()
    df = df.sort_index()
    return game, df


if __name__ == "__main__":
    g, p = main()
    print(p.groupby(level=1).get_group(10)[10:])
    # p.to_csv('optimal_policy.csv')
    # plt.plot(g.player._hit)
    # plt.plot(g.player._stay)
    # plt.show()
