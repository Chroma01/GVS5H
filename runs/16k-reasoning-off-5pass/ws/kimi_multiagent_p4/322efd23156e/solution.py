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
        v = int(next(it)); a = int(next(it)); c = int(next(it))
        groups[v - 1].append((a, c))

    # If any vitamin group is empty, we can never get >=1 of it.
    if any(len(g) == 0 for g in groups):
        print(0)
        return

    # For each vitamin: d[c] = max intake using at most c calories (0/1 knapsack).
    ds = []
    try:
        import numpy as np
        use_np = True
    except Exception:
        use_np = False

    for g in groups:
        if use_np:
            dp = np.zeros(X + 1, dtype=np.int64)
            for a, c in g:
                dp[c:] = np.maximum(dp[c:], dp[:-c] + a)
            # prefix max -> "at most c calories"
            dp = np.maximum.accumulate(dp)
            ds.append(dp)
        else:
            dp = [0] * (X + 1)
            for a, c in g:
                for cal in range(X, c - 1, -1):
                    val = dp[cal - c] + a
                    if val > dp[cal]:
                        dp[cal] = val
            for cal in range(1, X + 1):
                if dp[cal - 1] > dp[cal]:
                    dp[cal] = dp[cal - 1]
            ds.append(dp)

    # Min calories needed for vitamin v to reach intake >= T (None if impossible).
    def min_cal(d, T):
        if use_np:
            import numpy as np
            idx = int(np.searchsorted(d, T))
        else:
            idx = bisect_left(d, T)
        if idx > X:
            return None
        return idx

    # Upper bound for answer: smallest total A among groups.
    hi = min(sum(a for a, _ in g) for g in groups)
    lo = 0
    # Binary search largest feasible T.
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = 0
        ok = True
        for d in ds:
            mc = min_cal(d, mid)
            if mc is None:
                ok = False
                break
            total += mc
            if total > X:
                ok = False
                break
        if ok:
            lo = mid
        else:
            hi = mid - 1
    print(lo)

main()