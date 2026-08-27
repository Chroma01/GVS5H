import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    n = int(data[pos]); pos += 1
    X = int(data[pos]); pos += 1
    groups = [[], [], []]
    for _ in range(n):
        v = int(data[pos]); a = int(data[pos+1]); c = int(data[pos+2])
        pos += 3
        if c <= X:
            groups[v-1].append((a, c))

    try:
        import numpy as np
        use_np = True
    except Exception:
        use_np = False

    if use_np:
        def knap(items):
            dp = np.zeros(X + 1, dtype=np.int64)
            for a, c in items:
                if c > X:
                    continue
                dp[c:] = np.maximum(dp[c:], dp[:X + 1 - c] + a)
            np.maximum.accumulate(dp, out=dp)
            return dp

        f = [knap(g) for g in groups]

        hi = min(int(f[0][X]), int(f[1][X]), int(f[2][X]))

        def feasible(T):
            if T <= 0:
                return True
            tot = 0
            for arr in f:
                idx = int(np.searchsorted(arr, T, side='left'))
                if idx > X:
                    return False
                tot += idx
                if tot > X:
                    return False
            return tot <= X

    else:
        from bisect import bisect_left

        def knap(items):
            dp = [0] * (X + 1)
            for a, c in items:
                if c > X:
                    continue
                for j in range(X, c - 1, -1):
                    val = dp[j - c] + a
                    if val > dp[j]:
                        dp[j] = val
            best = 0
            for j in range(X + 1):
                if dp[j] > best:
                    best = dp[j]
                else:
                    dp[j] = best
            return dp

        f = [knap(g) for g in groups]
        hi = min(f[0][X], f[1][X], f[2][X])

        def feasible(T):
            if T <= 0:
                return True
            tot = 0
            for arr in f:
                idx = bisect_left(arr, T)
                if idx > X:
                    return False
                tot += idx
                if tot > X:
                    return False
            return tot <= X

    lo = 0
    # binary search largest T in [0, hi] with feasible(T)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

main()