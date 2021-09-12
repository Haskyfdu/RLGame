BossHp = [600, 800, 1000, 1200, 1000, 1000]
# 每个boss的血量

current_boss = {'id': 1, 'hp': 480}

mean_damage = [126, 138, 115, 112, 125, 130]
mean_num = [5, 6, 9, 11, 8, 8]


raw_ans = {}
for i in range(5):
    raw_ans[i+1] = 0

boss_id = current_boss['id']
num = current_boss['hp'] / mean_damage[boss_id-1]
raw_ans[boss_id] += num
boss_id += 1
if boss_id == 6:
    boss_id = 1


while num < 90:
    num += mean_num[boss_id-1]
    raw_ans[boss_id] += mean_num[boss_id-1]
    if num > 90:
        dif = num - 90
        raw_ans[boss_id] -= dif
    boss_id += 1
    if boss_id == 6:
        boss_id = 1


