import sys

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
        groups[v].append((c, a))

    sums = [0, 0, 0]
    for i in range(3):
        s = 0
        for _, a in groups[i]:
            s += a
        sums[i] = s
    if sums[0] == 0 or sums[1] == 0 or sums[2] == 0:
        sys.stdout.write("0\n")
        return

    try:
        import numpy as np
    except ImportError:
        np = None

    if np is not None:
        def min_cal(items, T):
            # min calories to obtain value >= T (0/1 knapsack), or None
            dp = np.zeros(X + 1, dtype=np.int64)
            for c, a in items:
                if a > T:
                    a = T
                # RHS fully evaluated before assignment -> correct 0/1 semantics
                np.maximum(dp[c:], dp[:X + 1 - c] + a, out=dp[c:])
                if dp[X] >= T:
                    # T is reachable; min calories may still drop with more
                    # items, but we can locate current best and keep going only
                    # if a cheaper reach is possible. Simplest: break is wrong
                    # for min calories, so don't break; but we can skip the
                    # final search cost by continuing. (No early break.)
                    pass
            idx = np.nonzero(dp >= T)[0]
            if idx.size == 0:
                return None
            return int(idx[0])
    else:
        def min_cal(items, T):
            dp = [0] * (X + 1)
            for c, a in items:
                if a > T:
                    a = T
                for j in range(X, c - 1, -1):
                    val = dp[j - c] + a
                    if val > dp[j]:
                        dp[j] = val
            for j in range(X + 1):
                if dp[j] >= T:
                    return j
            return None

    lo, hi = 0, min(sums)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        total = 0
        ok = True
        for g in groups:
            mc = min_cal(g, mid)
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
    sys.stdout.write(str(lo) + "\n")

main()