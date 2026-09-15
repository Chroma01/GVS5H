import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353
    letters = 'abcdefghijklmnopqrstuvwxyz'

    # State: tuple D[0..N] where D[i] = LCS(S[:i], T_prefix), D[0] = 0
    start = tuple([0] * (N + 1))

    trans_cache = {}

    def transition(state, c):
        key = (state, c)
        cached = trans_cache.get(key)
        if cached is not None:
            return cached
        new = [0] * (N + 1)
        for i in range(1, N + 1):
            eq = 1 if S[i - 1] == c else 0
            new[i] = max(new[i - 1], state[i], state[i - 1] + eq)
        res = tuple(new)
        trans_cache[key] = res
        return res

    dp = {start: 1}
    for _ in range(M):
        ndp = {}
        for state, cnt in dp.items():
            for c in letters:
                ns = transition(state, c)
                prev = ndp.get(ns, 0) + cnt
                if prev >= MOD:
                    prev -= MOD
                ndp[ns] = prev
        dp = ndp

    ans = [0] * (N + 1)
    for state, cnt in dp.items():
        ans[state[N]] = (ans[state[N]] + cnt) % MOD

    sys.stdout.write(' '.join(map(str, ans)) + '\n')

main()