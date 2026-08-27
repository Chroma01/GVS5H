import sys

MOD = 998244353


def solve():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    s = input().strip()

    size = 1 << n

    # transitions[mask] = list of (next_mask, number_of_characters)
    transitions = [[] for _ in range(size)]

    for mask in range(size):
        old = [0] * (n + 1)
        for i in range(n):
            old[i + 1] = old[i] + ((mask >> i) & 1)

        grouped = {}
        for ch_code in range(26):
            ch = chr(ord('a') + ch_code)
            new = [0] * (n + 1)

            for i in range(1, n + 1):
                if s[i - 1] == ch:
                    new[i] = old[i - 1] + 1
                else:
                    new[i] = max(old[i], new[i - 1])

            next_mask = 0
            for i in range(n):
                if new[i + 1] > new[i]:
                    next_mask |= 1 << i

            grouped[next_mask] = grouped.get(next_mask, 0) + 1

        transitions[mask] = list(grouped.items())

    dp = [0] * size
    dp[0] = 1

    for _ in range(m):
        ndp = [0] * size
        for mask, count in enumerate(dp):
            if count == 0:
                continue
            for next_mask, ways in transitions[mask]:
                ndp[next_mask] = (ndp[next_mask] + count * ways) % MOD
        dp = ndp

    ans = [0] * (n + 1)
    for mask, count in enumerate(dp):
        ans[mask.bit_count()] = (ans[mask.bit_count()] + count) % MOD

    print(*ans)


if __name__ == "__main__":
    solve()