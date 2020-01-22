from Warlock.class_Player_Warlock import PlayerWarlock


class GameWarlock:
    def __init__(self, boss_life):
        self.boss_life = boss_life
        self.boss_current_life = self.boss_life
        self.warlock = None

    def reset(self):
        self.boss_current_life = self.boss_life
        self.warlock = PlayerWarlock

