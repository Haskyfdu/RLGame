def next_step(state, n):
    if state[-1] != n:
        next_state = state
        next_state[-1] += 1
        return next_state
    else:
        i = len(state) - 1
        while i >= 0 and state[i] == n:
            i -= 1
        if i == -1:
            return None
        else:
            next_state = state[:i+1]
            next_state[-1] += 1
            return next_state


def check_state(state):
    p, j = len(state)-1, state[-1]
    for k, i in enumerate(state[:-1]):
        if i == j or abs(p-k) == abs(i-j):
            return False
    else:
        return True


def n_queens(n):
    ans, state = [], [1]
    while state is not None:
        if check_state(state):
            if len(state) == n:
                ans.append(state.copy())
                state = next_step(state, n)
            else:
                state.append(1)
        else:
            state = next_step(state, n)
    return ans


if __name__ == '__main__':

    q = n_queens(8)
