import sys
from bisect import bisect_left


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); X = int(data[pos + 1]); pos += 2

    groups = [[], [], [], []]  # grouped by vitamin 1..3
    for _ in range(n):
        v = int(data[pos]); a = int(data[pos + 1]); c = int(data[pos + 2]); pos += 3
        groups[v].append((a, c))

    f = [None] * 4          # f[v][c] = max vitamin v obtainable with <= c calories
    ub = None               # best answer upper bound = min over v of max reachable

    for v in (1, 2, 3):
        items = groups[v]

        # --- item reduction: for a fixed cost c, at most X//c copies can ever be
        # used, so keep only that many largest amounts. ---
        bycost = {}
        for a, c in items:
            if c in bycost:
                bycost[c].append(a)
            else:
                bycost[c] = [a]
        reduced = []
        for c, vals in bycost.items():
            lim = X // c
            if len(vals) > lim:
                vals.sort(reverse=True)
                vals = vals[:lim]
            for a in vals:
                reduced.append((a, c))

        # --- 0/1 knapsack over calories (at-most semantics via zero init) ---
        dp = [0] * (X + 1)
        for a, c in reduced:
            for cal in range(X, c - 1, -1):
                nv = dp[cal - c] + a
                if nv > dp[cal]:
                    dp[cal] = nv

        # --- enforce monotonicity so bisect is valid ---
        best = 0
        for cal in range(X + 1):
            d = dp[cal]
            if d > best:
                best = d
            else:
                dp[cal] = best

        f[v] = dp
        if ub is None or best < ub:
            ub = best

    # --- binary search the answer M (monotone: larger M needs >= calories) ---
    lo, hi = 0, ub
    ans = 0
    while lo <= hi:
        mid = (lo + hi) >> 1
        total = 0
        ok = True
        for v in (1, 2, 3):
            arr = f[v]
            idx = bisect_left(arr, mid)   # smallest calories reaching >= mid
            if idx > X:
                ok = False
                break
            total += idx
            if total > X:
                ok = False
                break
        if ok:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    sys.stdout.write(str(ans) + "\n")


main()