import sys
from bisect import bisect_left

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(map(int, data))
    n = next(it)
    x = next(it)

    groups = [[] for _ in range(3)]
    for _ in range(n):
        v = next(it) - 1
        a = next(it)
        c = next(it)
        groups[v].append((c, a))

    dps = []
    for items in groups:
        dp = [0] * (x + 1)

        if items:
            for c, a in items:
                for j in range(x, c - 1, -1):
                    nv = dp[j - c] + a
                    if nv > dp[j]:
                        dp[j] = nv

            best = 0
            for j in range(x + 1):
                if dp[j] < best:
                    dp[j] = best
                else:
                    best = dp[j]

        dps.append(dp)

    dp1, dp2, dp3 = dps
    bl = bisect_left

    def feasible(t):
        return bl(dp1, t) + bl(dp2, t) + bl(dp3, t) <= x

    lo = 0
    hi = min(dp1[x], dp2[x], dp3[x]) + 1

    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)

if __name__ == "__main__":
    solve()