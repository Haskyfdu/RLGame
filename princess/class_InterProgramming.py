#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------
# Copyright 2018 SAIC Artificial Intelligence Lab. All Rights Reserved.
# ----------------------------------------------------------------------

import pulp


class IntegerProgramming(object):

    # @classmethod
    # def pick_containers_wyq(cls, asss, origsumm, a, cost):
    #     if not (isinstance(origsumm, float) or isinstance(origsumm, int))
    #             or origsumm <= 0 or not isinstance(a, list) \
    #             or not isinstance(asss, list) or not len(a) == len(asss):
    #         print('Wrong Input')
    #         return
    #     if np.dot(a, asss) < origsumm:
    #         print('We need more cars.')
    #         return
    #     '''
    #     tic = datetime.now()
    #     '''
    #     global sbest, asssbest, di, asssk, costn
    #     summ = int(origsumm)
    #     di = len(a)
    #     if cost is None:
    #         cost = a
    #     dictt = dict(zip(a, asss))
    #     dicttpowerr = dict(zip(a, cost))
    #     an = sorted(a, reverse=True)
    #     ad = [int(summ / x) + 1 for x in an]
    #     asssn = [dictt[x] for x in an]
    #     asssm = min(asssn, ad)
    #     costn = [dicttpowerr[x] for x in an]
    #     sbest = summ * 100000  # ...
    #     asssbest = [0 for i in range(di)]
    #     asssk = [0 for i in range(di)]
    #
    #     def Iterate(noww, rangee, summleftt):
    #         global sbest, asssbest, di, asssk, costn
    #         if summleftt <= 0 or noww + 1 == di:
    #             asssk[noww] = max(0, math.ceil((summ - np.dot(an, asssk)) / an[noww]))
    #             sum_noww = np.dot(an, asssk)
    #             cost_now = np.dot(costn, asssk)
    #             if (asssk <= asssm) and (cost_now < sbest) and (summ <= sum_noww):
    #                 asssbest = copy.copy(asssk)
    #                 sbest = cost_now
    #             '''
    #             print('----------------------------')
    #             print('fini',noww)
    #             print(asssk, np.dot(an, asssk), summ)
    #             print(asssbest,sbest)
    #             '''
    #         else:
    #             for i in range(rangee, -1, -1):
    #                 asssk[noww] = i
    #                 inext = min(asssm[noww], int((summleftt - i * an[noww]) / an[noww]) + 1)
    #                 Iterate(noww + 1, inext, summleftt - i * an[noww])
    #
    #     Iterate(0, asssm[0], summ)
    #     '''
    #     print('============================')
    #     print('全部车型：', a)
    #     print('供应辆数：', asss)
    #     print('总需求量：', origsumm, '\ 95% =', summ)
    #     print('----------------------------')
    #     print('使用车型：', an)
    #     print('使用辆数：', asssbest)
    #     print('实际运量：', sbest)
    #     print('----------------------------')
    #     toc = datetime.now()
    #     print('总共用时', toc - tic)
    #     '''
    #     dictt2 = dict(zip(an, asssbest))
    #     res = [dictt2[x] for x in a]
    #     print('实际输出：', res, '总价: ', sbest)
    #     return res

    @classmethod
    def solve_ilp(cls, objective, constraints):
        # print(objective)
        # print(constraints)
        prob = pulp.LpProblem('LP1', pulp.LpMaximize)
        prob += objective
        for cons in constraints:
            prob += cons
        # print(prob)
        status = prob.solve()
        if status != 1:
            return None
        else:
            return [v.varValue.real for v in prob.variables()]

    @classmethod
    def pick_containers_1(cls, containers_num_up_bound, hp, cube_containers, cost=None):
        if cost is None:
            cost = cube_containers
        kinds = len(containers_num_up_bound)
        # variables, set low/up bound
        variables = [pulp.LpVariable('X%d' % i, lowBound=0, upBound=containers_num_up_bound[i],
                                     cat=pulp.LpInteger) for i in range(0, kinds)]
        # objective function
        objective = -sum([cost[i] * variables[i] for i in range(0, kinds)])
        # constrained condition
        constraints = [sum([cube_containers[i] * variables[i] for i in range(0, kinds)]) >= hp]
        # print(constraints)
        res = cls.solve_ilp(objective, constraints)
        return res

    @classmethod
    def pick_containers_2(cls, containers_num_up_bound, hp, cube_containers, cost=None):
        if cost is None:
            cost = cube_containers
        kinds = len(containers_num_up_bound)
        # variables, set low/up bound
        variables = [pulp.LpVariable('X%d' % i, lowBound=0, upBound=containers_num_up_bound[i],
                                     cat=pulp.LpInteger) for i in range(0, kinds)]
        # objective function
        objective = sum([cost[i] * variables[i] for i in range(0, kinds)])
        # constrained condition
        constraints = [sum([cube_containers[i] * variables[i] for i in range(0, kinds)]) <= hp]
        # print(constraints)
        res = cls.solve_ilp(objective, constraints)
        return res


if __name__ == '__main__':

    a = 1
# cube = sum([container[i]['length'] * container[i]['width'] * container_use_num_list[i]
#                         for i in range(len(container))])
#             container_use_num_list = IntegerProgramming.pick_containers(containers_num_up_bound, cube+1,
#                                                                         cube_containers, cost=None)
