import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    N = int(data[0])
    X = int(data[1])
    groups = [[], [], []]
    idx = 2
    for _ in range(N):
        v = int(data[idx]) - 1
        a = int(data[idx + 1])
        c = int(data[idx + 2])
        groups[v].append((a, c))
        idx += 3

    best = []
    for g in groups:
        total_cost = 0
        for _, c in g:
            total_cost += c
        limit = X if total_cost > X else total_cost
        dp = [0] * (limit + 1)
        for a, c in g:
            for j in range(limit, c - 1, -1):
                val = dp[j - c] + a
                if val > dp[j]:
                    dp[j] = val
        if limit < X:
            dp.extend([dp[limit]] * (X - limit))
        best.append(dp)

    hi = min(best[0][X], best[1][X], best[2][X])
    lo = 0

    def feasible(t):
        total = 0
        for dp in best:
            pos = bisect_left(dp, t)
            if pos > X:
                return False
            total += pos
            if total > X:
                return False
        return True

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)

if __name__ == "__main__":
    main()