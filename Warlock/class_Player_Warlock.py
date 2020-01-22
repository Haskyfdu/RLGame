class PlayerWarlock:
    def __init__(self, warlock_life=30000):
        self.life = warlock_life
        # intellect, citical, haste, mastery, versatility,
        # self.intellect = intellect
        # self.citical = citical
        # self.haste = haste
        # self.mastery = mastery
        # self.versatility = versatility
        self.position = [0, 0]
        self.ashes = 2.0
        self.gcd = 1.0                  # global cool down
        self.cd = {'deflagration': 0, 'dark_soul': 0}
        self.buff = {'deflagration_buff': {'available_times': 0, 'remaining_duration': 0},
                     'dark_soul_buff': {'remaining_duration': 0}}

    # def choice_origin_position(self):
    #     pass
    #
    # def move(self, direction):
    #     # ['forward', 'back', 'left', 'right']
    #     if direction == 'forward':
    #         self.position[1] += 1
    #     elif direction == 'back':
    #         self.position[1] -= 1
    #     elif direction == 'left':
    #         self.position[0] -= 1
    #     elif direction == 'right':
    #         self.position[0] += 1
    #     else:
    #         raise ValueError('Move in an unknown direction.')

    """脑残箭"""
    def chaos_bolt(self):
        if self.ashes >= 2:
            self.ashes -= 2
        else:
            raise ValueError('Your ashes are insufficient.')
        damage = 3000
        cast_time = 2.0
        if self.buff['dark_soul_buff']['remaining_duration'] > cast_time:
            damage *= 1.5
        return {'damage': damage, 'caat_time': cast_time}

    """爆燃"""
    def deflagration(self):
        self.ashes = max(5, self.ashes+0.3)
        damage = 500
        cast_time = 0
        self.buff['deflagration_buff'] = {'available_times': 2, 'remaining_duration': 30}
        self.cd['deflagration'] = 8
        return {'damage': damage, 'caat_time': cast_time}

    """烧尽"""
    def burn_out(self):
        self.ashes = max(5, self.ashes + 0.2)
        damage = 500
        cast_time = 1
        if self.buff['deflagration_buff']['available_times'] > 0:
            cast_time *= 0.6
            self.buff['deflagration_buff']['available_times'] -= 1
        return {'damage': damage, 'caat_time': cast_time}

    def dark_soul(self):
        damage = 0
        cast_time = 0
        self.cd['dark_soul'] = 120
        self.buff['dark_soul_buff']['remaining_duration'] = 25
        return {'damage': damage, 'caat_time': cast_time}

    # """献祭 dot"""
    # def immolate(self):
    #     pass
    #
    # """火雨 aoe"""
    # def rain_of_fire(self):
    #     pass
    #
    # """吸血"""
    # def drain_life(self):
    #     pass
    # def interrupt_cast(self):
    #     pass
