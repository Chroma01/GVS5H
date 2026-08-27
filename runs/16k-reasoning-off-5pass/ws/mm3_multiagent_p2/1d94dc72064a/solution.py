from functools import lru_cache
import sys
sys.setrecursionlimit(100000)

def solve_small():
    from itertools import product

    maxA = 4
    results = {}

    def get_moves(state):
        # state is a tuple of (a_i, opened) for i=0..N-1
        moves = []
        N = len(state)
        for i in range(N):
            if state[i][0] == 0:
                continue
            new_state = list(state)
            a, op = new_state[i]
            new_a = a - 1
            new_op = op
            if op == 0:
                new_op = 1
            new_state[i] = (new_a, new_op)
            if all(s[1] == 1 for s in new_state):
                moves.append('win')
            else:
                moves.append(tuple(new_state))
        return moves

    memo = {}
    def is_winning(state):
        # state is a tuple of (a_i, op)
        if all(s[1] == 1 for s in state):
            return False  # shouldn't happen, but treat as losing for player to move
        if state in memo:
            return memo[state]
        moves = get_moves(state)
        for m in moves:
            if m == 'win':
                memo[state] = True
                return True
            if not is_winning(m):
                memo[state] = True
                return True
        memo[state] = False
        return False

    for N in [1,2,3]:
        for vals in product(range(1, maxA+1), repeat=N):
            state = tuple((v, 0) for v in vals)
            win = is_winning(state)
            results[vals] = win
            print(f"N={N}, A={vals}: {'Fennec' if win else 'Snuke'}")

    print("\nChecking hypotheses:")
    for vals, win in results.items():
        xor_minus1 = 0
        for v in vals:
            xor_minus1 ^= (v-1)
        xor_v = 0
        for v in vals:
            xor_v ^= v
        num_odd = sum(1 for v in vals if v%2==1)
        num_gt1 = sum(1 for v in vals if v>1)
        sum_v = sum(vals)
        sum_minus1 = sum_v - len(vals)
        N = len(vals)
        num_ones = sum(1 for v in vals if v == 1)
        print(f"A={vals}, win={win}, xor(A-1)={xor_minus1}, xor(A)={xor_v}, num_odd={num_odd}, num_gt1={num_gt1}, sum={sum_v}, sum-N={sum_minus1}, N%2={N%2}, num_ones={num_ones}")

solve_small()