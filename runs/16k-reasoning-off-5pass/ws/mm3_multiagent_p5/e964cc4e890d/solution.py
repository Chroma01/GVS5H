import sys
sys.setrecursionlimit(1 << 25)

MOD = 998244353

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].decode().strip()
    s = '#' + S

    memo = {}

    def dp(l, r):
        if l > r:
            return 1
        if l == r:
            return 0
        if (l, r) in memo:
            return memo[(l, r)]
        if s[l] != 'B' or s[r] != 'W':
            memo[(l, r)] = 0
            return 0
        total = 0
        for k in range(l + 1, r + 1):
            if s[k] != 'W':
                continue
            left = dp(l + 1, k - 1)
            right = dp(k + 1, r)
            total = (total + left * right) % MOD
        memo[(l, r)] = total
        return total

    print(dp(1, 2 * N) % MOD)

if __name__ == "__main__":
    solve()