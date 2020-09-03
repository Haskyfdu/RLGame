from matplotlib import pyplot as plt


def sijiamaibaoxian(rate):
    print('利率： ' + str(round((rate-1)*100, 2)) + '%')
    year = 30
    price = 8599.97+137.17+430.86
    cost = round(sum([price/(rate**k) for k in range(year)]), 2)
    print('友邦 '+str(year)+'年: '+str(cost))

    year1 = 30
    price1 = 6055
    cost1 = round(sum([price1/(rate**k) for k in range(year1)]), 2)
    print('超级玛丽 '+str(year1)+'年: '+str(cost1))

    print('贵了'+str(round((cost/cost1-1)*100, 2))+'%')
    return round((cost/cost1-1)*100, 2)


sijiamaibaoxian(1.045)

x = []
y = []
for r in range(100):
    m = r/1000 + 1
    n = sijiamaibaoxian(m)
    x.append(m)
    y.append(n)
plt.plot(x, y)
plt.show()
