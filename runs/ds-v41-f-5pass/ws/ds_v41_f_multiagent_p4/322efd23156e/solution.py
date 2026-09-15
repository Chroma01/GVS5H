import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos]); pos += 1
    X = int(data[pos]); pos += 1

    items = [[], [], [], []]  # index by vitamin 1..3
    for _ in range(n):
        v = int(data[pos]); a = int(data[pos + 1]); c = int(data[pos + 2])
        pos += 3
        items[v].append((c, a))

    try:
        import numpy as np
    except ImportError:
        np = None

    dps = []  # dps[v-1][c] = max units of vitamin v with calorie cost <= c

    if np is not None:
        for v in range(1, 4):
            dp = np.zeros(X + 1, dtype=np.int64)
            for c, a in items[v]:
                if c <= X:
                    # 0/1 update using old dp values for every capacity at once
                    np.maximum(dp[c:], dp[:X + 1 - c] + a, out=dp[c:])
            np.maximum.accumulate(dp, out=dp)  # ensure nondecreasing
            dps.append(dp.tolist())
    else:
        for v in range(1, 4):
            dp = [0] * (X + 1)
            for c, a in items[v]:
                if c <= X:
                    for cap in range(X, c - 1, -1):
                        val = dp[cap - c] + a
                        if val > dp[cap]:
                            dp[cap] = val
            m = 0
            for i in range(X + 1):
                if dp[i] < m:
                    dp[i] = m
                else:
                    m = dp[i]
            dps.append(dp)

    upper = min(dp[X] for dp in dps)

    def total_cost(K):
        s = 0
        for dp in dps:
            s += bisect_left(dp, K)  # min calories to reach >= K
            if s > X:
                return s
        return s

    lo, hi = 0, upper + 1  # lo always feasible, hi infeasible sentinel
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if total_cost(mid) <= X:
            lo = mid
        else:
            hi = mid

    sys.stdout.write(str(lo) + "\n")


main()