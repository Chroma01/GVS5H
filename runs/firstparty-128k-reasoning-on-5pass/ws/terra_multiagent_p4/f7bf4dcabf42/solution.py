import sys
from collections import defaultdict

MOD = 998244353

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    S = input().strip()

    transition_cache = {}

    def transitions(state):
        if state in transition_cache:
            return transition_cache[state]

        grouped = {}
        for ch in range(26):
            row = [0] * (N + 1)
            for j in range(1, N + 1):
                if ord(S[j - 1]) - 97 == ch:
                    row[j] = state[j - 1] + 1
                else:
                    row[j] = max(state[j], row[j - 1])
            nxt = tuple(row)
            grouped[nxt] = grouped.get(nxt, 0) + 1

        result = list(grouped.items())
        transition_cache[state] = result
        return result

    initial = tuple([0] * (N + 1))
    dp = {initial: 1}

    for _ in range(M):
        ndp = defaultdict(int)
        for state, count in dp.items():
            for nxt, multiplicity in transitions(state):
                ndp[nxt] = (ndp[nxt] + count * multiplicity) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for state, count in dp.items():
        ans[state[N]] = (ans[state[N]] + count) % MOD

    print(*ans)

if __name__ == "__main__":
    solve()