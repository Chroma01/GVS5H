import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    S = input().strip()

    zero = (0,) * (N + 1)
    states = [zero]
    state_id = {zero: 0}
    transitions = []

    pos = 0
    while pos < len(states):
        row = states[pos]
        grouped = {}

        for c in range(26):
            nxt = [0] * (N + 1)
            ch = chr(ord('a') + c)

            for j in range(1, N + 1):
                if ch == S[j - 1]:
                    nxt[j] = row[j - 1] + 1
                else:
                    nxt[j] = max(row[j], nxt[j - 1])

            nxt = tuple(nxt)
            dest = state_id.get(nxt)
            if dest is None:
                dest = len(states)
                state_id[nxt] = dest
                states.append(nxt)

            grouped[dest] = grouped.get(dest, 0) + 1

        transitions.append(list(grouped.items()))
        pos += 1

    count = len(states)
    dp = [0] * count
    dp[0] = 1

    for _ in range(M):
        ndp = [0] * count
        for state, ways in enumerate(dp):
            if ways == 0:
                continue
            for dest, multiplicity in transitions[state]:
                ndp[dest] = (ndp[dest] + ways * multiplicity) % MOD
        dp = ndp

    answer = [0] * (N + 1)
    for state, ways in enumerate(dp):
        lcs = states[state][N]
        answer[lcs] = (answer[lcs] + ways) % MOD

    print(*answer)

if __name__ == "__main__":
    solve()