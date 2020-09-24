import json
import pandas as pd
from priecess.class_InterProgramming import IntegerProgramming

BossHp = [600, 800, 1000, 1200, 1000, 1000]
# 每个boss的血量

df1 = pd.read_excel('8.26box统计.xlsx', sheet_name='box', header=0)
box = df1.to_dict(orient='records')
# 每个人的box，各个角色的等级

used_box = {}
for p in box:
    q = {}
    for c in p:
        q[c] = 1
    # q['猫拳/暴击弓/病娇'] = int(p['猫拳'] == 5) + int(p['暴击弓'] == 5) + int(p['病娇'] == 5)
    q['猫拳/暴击弓/病娇'] = 3
    p['猫拳/暴击弓/病娇'] = max(p['猫拳'], p['暴击弓'], p['病娇'])
    name = p['昵称']
    used_box[name]=q
# 记录每个人每个角色使用次数，关键用于多选角色的阵容可配置

df1 = pd.read_excel('8.26box统计.xlsx', sheet_name='阵容', header=0)
team_box = df1.to_dict(orient='records')
# 记录每个boss可用的阵容以及对应的预期伤害

mix_team = {1: team_box[0]}
for i in range(2, 6):
    mix_team[i] = team_box[1]

team_list = []
for team_info in team_box:
    team = {}
    for i in range(1, 6):
        team[team_info['角色'+str(i)]] = team_info['角色'+str(i)+'要求']
    team['boss'] = team_info['boss']
    team['damage'] = team_info['预期伤害']
    team_list.append(team)


current_boss = {'id': 1, 'hp': 600}
left_turn = 90
raw_result = []
turn_count = 1
result = []

while left_turn > 0:

    available_team = [p for p in team_list if p['boss'] == current_boss['id']]
    # 对应boss的可用阵容
    damage_list = [p['damage'] for p in available_team]
    # 对应boss可用阵容的预期伤害

    left_num = []
    for p in available_team:
        num = 0
        for b in box:
            flag = 0
            for c in p:
                if c not in ['boss', 'damage']:
                    if b[c] < p[c] or used_box[b['昵称']][c] == 0:
                        flag += 1
                    if flag >= 2:
                        break
            if flag <= 1:
                num += 1
        left_num.append(num)

    team_num_1 = IntegerProgramming.pick_containers_1(left_num, current_boss['hp'], damage_list)
    team_num_2 = IntegerProgramming.pick_containers_2(left_num, current_boss['hp'], damage_list)

    if team_num_1 is None:
        print(turn_count, left_num, current_boss, damage_list)
    dif1 = current_boss['hp'] - sum([damage_list[i] * team_num_2[i] for i in range(len(team_num_2))])
    dif2 = sum([damage_list[i] * team_num_1[i] for i in range(len(team_num_1))]) - current_boss['hp']

    if dif1 < dif2:
        # boss 还有一丝血，用下一个boss的阵容来和这个boss输出最高的阵容一起合刀
        round_team = team_num_1
    elif dif2 <= dif1:
        # 伤害溢出，伤害最高的两刀在最后合刀，打得低的那一个收尾，蹭一蹭下一个boss
        round_team = team_num_2
    else:
        raise ValueError('bug')

    for i in range(len(round_team)):
        team = available_team[i]
        num = round_team[i]
        for person_box in box:
            if num == 0:
                break
            name = person_box['昵称']
            lack = []
            for c in team:
                if c not in ['damage', 'boss']:
                    if person_box[c] < team[c] or used_box[name][c] <= 0:
                        lack.append(c)
                    if len(lack) >= 2:
                        break
            if len(lack) <= 1:
                fright_team = []
                for c in team:
                    if c not in ['damage', 'boss']+lack:
                        fright_team.append(c)
                        used_box[name][c] -= 1
                        if c in ['猫拳', '暴击弓', '病娇']:
                            used_box[name]['猫拳/暴击弓/病娇'] -= 1
                result.append({'昵称': name,
                               '阵容': fright_team,
                               '租借角色': lack,
                               '出刀编号': turn_count,
                               'Boss编号': team['boss'],
                               '预计伤害': team['damage']})
                turn_count += 1
                num -= 1

    left_turn -= sum(round_team)
    raw_result.append(round_team)
    current_boss['id'] += 1
    if current_boss['id'] >= 7:
        current_boss['id'] = 1
    current_boss['hp'] = BossHp[current_boss['id'] - 1]

