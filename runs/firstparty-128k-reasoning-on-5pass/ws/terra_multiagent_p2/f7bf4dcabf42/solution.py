import sys

MOD = 998244353


def solve():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    s = data[2]

    state_count = 1 << n
    transitions = [[] for _ in range(state_count)]

    for mask in range(state_count):
        old = [0] * (n + 1)
        for j in range(1, n + 1):
            old[j] = old[j - 1] + ((mask >> (j - 1)) & 1)

        counts = {}
        for ch in range(26):
            new = [0] * (n + 1)
            for j in range(1, n + 1):
                if ord(s[j - 1]) - ord('a') == ch:
                    new[j] = old[j - 1] + 1
                else:
                    new[j] = max(old[j], new[j - 1])

            nxt_mask = 0
            for j in range(1, n + 1):
                if new[j] > new[j - 1]:
                    nxt_mask |= 1 << (j - 1)
            counts[nxt_mask] = counts.get(nxt_mask, 0) + 1

        transitions[mask] = list(counts.items())

    dp = [0] * state_count
    dp[0] = 1

    for _ in range(m):
        ndp = [0] * state_count
        for mask, value in enumerate(dp):
            if value == 0:
                continue
            for nxt_mask, multiplicity in transitions[mask]:
                ndp[nxt_mask] = (ndp[nxt_mask] + value * multiplicity) % MOD
        dp = ndp

    ans = [0] * (n + 1)
    for mask, value in enumerate(dp):
        ans[mask.bit_count()] = (ans[mask.bit_count()] + value) % MOD

    print(*ans)


if __name__ == "__main__":
    solve()