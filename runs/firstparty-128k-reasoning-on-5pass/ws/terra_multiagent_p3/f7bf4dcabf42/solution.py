import sys

MOD = 998244353

def solve():
    input = sys.stdin.readline
    N, M = map(int, input().split())
    S = input().strip()

    trans_cache = {}

    def next_mask(mask, ch):
        key = (mask, ch)
        if key in trans_cache:
            return trans_cache[key]

        prev = [0] * (N + 1)
        for i in range(N):
            prev[i + 1] = prev[i] + ((mask >> i) & 1)

        cur = [0] * (N + 1)
        new_mask = 0
        for i in range(1, N + 1):
            if S[i - 1] == ch:
                cur[i] = max(prev[i - 1] + 1, prev[i], cur[i - 1])
            else:
                cur[i] = max(prev[i], cur[i - 1])
            if cur[i] > cur[i - 1]:
                new_mask |= 1 << (i - 1)

        trans_cache[key] = new_mask
        return new_mask

    dp = {0: 1}

    for _ in range(M):
        ndp = {}
        for mask, count in dp.items():
            for c in range(26):
                nxt = next_mask(mask, chr(ord('a') + c))
                ndp[nxt] = (ndp.get(nxt, 0) + count) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for mask, count in dp.items():
        lcs_length = mask.bit_count()
        ans[lcs_length] = (ans[lcs_length] + count) % MOD

    print(*ans)

if __name__ == "__main__":
    solve()