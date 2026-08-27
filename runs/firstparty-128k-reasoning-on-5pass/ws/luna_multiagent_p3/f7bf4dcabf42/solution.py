import sys
from collections import defaultdict

MOD = 998244353


def main():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    S = input().strip()

    start = (0,) * (N + 1)
    transition_cache = {}

    def transitions(state):
        if state in transition_cache:
            return transition_cache[state]

        counts = defaultdict(int)
        for c in range(26):
            nxt = [0] * (N + 1)
            for j in range(1, N + 1):
                best = max(state[j], nxt[j - 1])
                if S[j - 1] == chr(ord('a') + c):
                    best = max(best, state[j - 1] + 1)
                nxt[j] = best
            counts[tuple(nxt)] += 1

        result = list(counts.items())
        transition_cache[state] = result
        return result

    dp = {start: 1}

    for _ in range(M):
        ndp = defaultdict(int)
        for state, ways in dp.items():
            for nxt, multiplicity in transitions(state):
                ndp[nxt] = (ndp[nxt] + ways * multiplicity) % MOD
        dp = ndp

    answer = [0] * (N + 1)
    for state, ways in dp.items():
        answer[state[N]] = (answer[state[N]] + ways) % MOD

    print(*answer)


if __name__ == "__main__":
    main()