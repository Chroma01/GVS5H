import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])
    s = data[2]

    size = 1 << n
    transitions = [[0] * 26 for _ in range(size)]

    for mask in range(size):
        old = [0] * (n + 1)
        for j in range(n):
            old[j + 1] = old[j] + ((mask >> j) & 1)

        for ch in range(26):
            new = [0] * (n + 1)
            for j in range(1, n + 1):
                if ord(s[j - 1]) - 97 == ch:
                    new[j] = old[j - 1] + 1
                else:
                    new[j] = max(old[j], new[j - 1])

            nxt_mask = 0
            for j in range(n):
                if new[j + 1] > new[j]:
                    nxt_mask |= 1 << j
            transitions[mask][ch] = nxt_mask

    dp = [0] * size
    dp[0] = 1

    for _ in range(m):
        ndp = [0] * size
        for mask, count in enumerate(dp):
            if count == 0:
                continue
            for ch in range(26):
                nxt = transitions[mask][ch]
                ndp[nxt] += count
                if ndp[nxt] >= MOD:
                    ndp[nxt] -= MOD
        dp = ndp

    ans = [0] * (n + 1)
    for mask, count in enumerate(dp):
        ans[mask.bit_count()] += count
        if ans[mask.bit_count()] >= MOD:
            ans[mask.bit_count()] -= MOD

    print(*ans)


if __name__ == "__main__":
    main()