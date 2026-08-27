from typing import List

try:
    import numpy as _np
except Exception:  # pragma: no cover
    _np = None


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        L = 4 * side

        def to_perimeter(x, y):
            if y == 0:
                return x
            if x == side:
                return side + y
            if y == side:
                return 3 * side - x
            return 4 * side - y

        pos = sorted(to_perimeter(x, y) for x, y in points)
        n = len(pos)

        hi = L // k
        if hi < 1:
            hi = 1
        lo = 1

        if _np is not None:
            np = _np
            posA = np.array(pos, dtype=np.int64)
            pos2 = np.concatenate((posA, posA + L))              # size 2n, strictly increasing
            m = 2 * n
            INF = np.int64(1 << 62)
            posext = np.concatenate((pos2, np.array([INF], dtype=np.int64)))  # size 2n+1
            starts = np.arange(n, dtype=np.int64)
            limit = posA + L                                     # pos[i] + L

            def feasible(d):
                nxt = np.searchsorted(pos2, pos2 + d, side='left').astype(np.int64)
                nxt_full = np.concatenate((nxt, np.array([m], dtype=np.int64)))
                cur = starts
                for _ in range(k - 1):
                    cur = nxt_full[cur]
                return bool(np.any(posext[cur] + d <= limit))
        else:
            pos2 = pos + [p + L for p in pos]
            m = 2 * n

            def feasible(d):
                nxt = [0] * (m + 1)
                j = 0
                for i in range(m):
                    if j < i:
                        j = i
                    target = pos2[i] + d
                    while j < m and pos2[j] < target:
                        j += 1
                    nxt[i] = j
                nxt[m] = m
                steps = k - 1
                cur = list(range(n))
                table = nxt
                while steps:
                    if steps & 1:
                        cur = [table[c] for c in cur]
                    steps >>= 1
                    if steps:
                        table = [table[t] for t in table]
                for i in range(n):
                    c = cur[i]
                    if c < m and pos2[c] + d <= pos[i] + L:
                        return True
                return False

        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return int(lo)


# ---------------------------------------------------------------------------
# Test harness (Task E).  Only runs when executed as a script.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import random
    import time
    from itertools import combinations

    def brute(side, points, k):
        best = 0
        for comb in combinations(points, k):
            mn = min(abs(a[0] - b[0]) + abs(a[1] - b[1])
                     for a, b in combinations(comb, 2))
            if mn > best:
                best = mn
        return best

    def all_boundary(side):
        pts = set()
        for x in range(side + 1):
            pts.add((x, 0))
            pts.add((x, side))
        for y in range(side + 1):
            pts.add((0, y))
            pts.add((side, y))
        return sorted(pts)

    s = Solution()

    # provided examples
    assert s.maxDistance(2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4) == 2
    assert s.maxDistance(2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4) == 1
    assert s.maxDistance(2, [[0, 0], [0, 1], [0, 2], [1, 2],
                             [2, 0], [2, 2], [2, 1]], 5) == 1

    random.seed(12345)
    fails = 0
    trials = 0
    for _ in range(600):
        side = random.randint(1, 6)
        pool = all_boundary(side)
        if len(pool) < 4:
            continue
        n = random.randint(4, min(12, len(pool)))
        pts = [list(p) for p in random.sample(pool, n)]
        k = random.randint(4, min(6, n))
        trials += 1
        exp = brute(side, [tuple(p) for p in pts], k)
        got = s.maxDistance(side, [list(p) for p in pts], k)
        if got != exp:
            fails += 1
            print("MISMATCH", side, pts, k, "expected", exp, "got", got)
    print("random tests (numpy path):", trials, "cases,", fails, "failures")

    # degenerate cases
    deg = [
        (1, [[0, 0], [1, 0], [1, 1], [0, 1]], 4),
        (5, [[0, 0], [5, 0], [5, 5], [0, 5]], 4),
        (6, [[x, 0] for x in range(7)], 4),
        (6, [[x, 0] for x in range(7)], 6),
        (4, [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [4, 1], [4, 2]], 4),
        (3, all_boundary(3)[:8], 8),
    ]
    for side, pts, k in deg:
        pts = [list(p) for p in pts]
        if len(pts) >= k:
            exp = brute(side, [tuple(p) for p in pts], k)
            got = s.maxDistance(side, [list(p) for p in pts], k)
            if exp != got:
                print("DEG MISMATCH", side, pts, k, exp, got)
    print("degenerate cases done")

    # pure-python fallback path
    globals()['_np'] = None
    random.seed(999)
    fails = 0
    trials = 0
    for _ in range(300):
        side = random.randint(1, 6)
        pool = all_boundary(side)
        if len(pool) < 4:
            continue
        n = random.randint(4, min(12, len(pool)))
        pts = [list(p) for p in random.sample(pool, n)]
        k = random.randint(4, min(6, n))
        trials += 1
        exp = brute(side, [tuple(p) for p in pts], k)
        got = s.maxDistance(side, [list(p) for p in pts], k)
        if got != exp:
            fails += 1
            print("FALLBACK MISMATCH", side, pts, k, "expected", exp, "got", got)
    print("random tests (fallback path):", trials, "cases,", fails, "failures")
    globals()['_np'] = _np if _np is not None else None
    try:
        import numpy as _restore
        globals()['_np'] = _restore
    except Exception:
        pass

    # perf check
    side = 10 ** 9
    L = 4 * side
    ts = random.sample(range(L), 15000)
    big = []
    for t in ts:
        if t < side:
            big.append([t, 0])
        elif t < 2 * side:
            big.append([side, t - side])
        elif t < 3 * side:
            big.append([3 * side - t, side])
        else:
            big.append([0, 4 * side - t])
    st = time.time()
    ans = s.maxDistance(side, big, 25)
    print("perf n=15000 k=25:", ans, "in %.3fs" % (time.time() - st))