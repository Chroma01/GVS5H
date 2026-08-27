import sys
from bisect import bisect_left

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))

    groups = [[], [], []]
    for _ in range(N):
        v = int(next(it)) - 1
        a = int(next(it))
        c = int(next(it))
        groups[v].append((a, c))

    # If any vitamin group is empty, answer is 0
    if any(len(g) == 0 for g in groups):
        print(0)
        return

    NEG = -1
    bests = []
    for g in groups:
        # dp[c] = max intake achievable with exactly c calories (0/1 knapsack)
        dp = [NEG] * (X + 1)
        dp[0] = 0
        for a, c in groups.index(g) if False else g:
            if c > X:
                continue
            # descending iteration for 0/1 knapsack
            for cal in range(X - c, -1, -1):
                prev = dp[cal]
                if prev != NEG:
                    val = prev + a
                    if val > dp[cal + c]:
                        dp[cal + c] = val
        # best[c] = max intake with at most c calories (prefix max, monotone)
        best = dp[:]
        for i in range(1, X + 1):
            if best[i] < best[i - 1]:
                best[i] = best[i - 1]
        bests.append(best)

    # min calories for group g to reach intake >= T: bisect on monotone best
    INF = float('inf')
    def min_cal(g, T):
        b = bests[g]
        if b[X] < T:
            return INF
        return bisect_left(b, T)

    # Binary search on T
    # hi = min over groups of total intake in that group
    hi = min(sum(a for a, _ in g) for g in groups)
    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = min_cal(0, mid) + min_cal(1, mid) + min_cal(2, mid)
        if total <= X:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

main()