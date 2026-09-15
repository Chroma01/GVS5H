from typing import List
import time
import random
import itertools
from math import comb


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        S = side
        L = 4 * S

        # Map each boundary point onto a position on the cycle of length L = 4*side.
        # bottom (x,0) -> x ; right (side,y) -> side+y ;
        # top (x,side) -> 2*side+(side-x) ; left (0,y) -> 3*side+(side-y)
        pos = []
        for x, y in points:
            if y == 0:
                pos.append(x)
            elif y == S:
                pos.append(2 * S + (S - x))
            elif x == 0:
                pos.append(3 * S + (S - y))
            else:
                pos.append(S + y)
        pos.sort()
        n = len(pos)
        m = 2 * n
        pos2 = pos + [p + L for p in pos]   # doubled, strictly increasing

        need = k - 1
        levels = max(1, need.bit_length())

        def feasible(D):
            # Can we choose k cycle positions with all pairwise cyclic distances >= D ?
            if D <= 0 or need == 0:
                return True
            if n < k:
                return False
            # nxt[i] = first index j with pos2[j] >= pos2[i] + D  (monotone two pointers)
            nxt = [m] * (m + 1)
            j = 0
            for i in range(m):
                if j < i:
                    j = i
                tgt = pos2[i] + D
                while j < m and pos2[j] < tgt:
                    j += 1
                nxt[i] = j
            # binary lifting over the greedy successor function
            jp = [nxt]
            for _ in range(levels - 1):
                prev = jp[-1]
                jp.append([prev[prev[t]] for t in range(m + 1)])
            # start i: take earliest feasible next point each time; the last one must
            # still be at position <= pos2[i] + L - D so the wrap-around gap is >= D.
            for i in range(n):
                deadline = pos2[i] + L - D
                cur = i
                b = need
                lv = 0
                while b:
                    if b & 1:
                        cur = jp[lv][cur]
                        if cur >= m:
                            break
                    b >>= 1
                    lv += 1
                if cur < m and pos2[cur] <= deadline:
                    return True
            return False

        # For k >= 4 the answer never exceeds side, so binary search on [0, side].
        lo, hi, ans = 0, S, 0
        while lo <= hi:
            mid = (lo + hi) >> 1
            if feasible(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans


# ---------------------------------------------------------------------------
# Validation harness
# ---------------------------------------------------------------------------

def brute_force(side, points, k):
    n = len(points)
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            d = abs(xi - xj) + abs(yi - yj)
            dist[i][j] = d
            dist[j][i] = d
    best = 0
    for sub in itertools.combinations(range(n), k):
        mn = 10 ** 18
        for a in range(k):
            da = dist[sub[a]]
            for b in range(a + 1, k):
                if da[sub[b]] < mn:
                    mn = da[sub[b]]
        if mn > best:
            best = mn
    return best


def boundary_points(side):
    pts = set()
    for x in range(side + 1):
        pts.add((x, 0))
        pts.add((x, side))
    for y in range(side + 1):
        pts.add((0, y))
        pts.add((side, y))
    return sorted(pts)


def gen_random_boundary(side, n, rng):
    pts = set()
    while len(pts) < n:
        w = rng.randrange(4)
        c = rng.randrange(side + 1)
        if w == 0:
            pts.add((c, 0))
        elif w == 1:
            pts.add((c, side))
        elif w == 2:
            pts.add((0, c))
        else:
            pts.add((side, c))
    return [list(p) for p in pts]


def gen_bottom_edge(side, n, rng):
    xs = rng.sample(range(side + 1), n)
    return [[x, 0] for x in xs]


def main():
    sol = Solution()
    rng = random.Random(20240517)

    examples = [
        (2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4, 2),
        (2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4, 1),
        (2, [[0, 0], [0, 1], [0, 2], [1, 2], [2, 0], [2, 2], [2, 1]], 5, 1),
    ]
    sample_ok = True
    print("=== SAMPLE TESTS ===")
    for i, (side, pts, k, exp) in enumerate(examples, 1):
        got = sol.maxDistance(side, [list(p) for p in pts], k)
        ok = got == exp
        sample_ok = sample_ok and ok
        print("Example %d: got=%d expected=%d -> %s" % (i, got, exp, "PASS" if ok else "FAIL"))
    print("SAMPLE TESTS OVERALL:", "PASS" if sample_ok else "FAIL")

    print("=== STRESS TEST ===")
    trials = 0
    fails = 0
    t0 = time.time()
    for _ in range(600):
        side = rng.randint(1, 4)
        allpts = boundary_points(side)
        n = rng.randint(4, len(allpts))
        pts = rng.sample(allpts, n)
        k = rng.randint(4, min(25, n))
        if comb(n, k) * comb(k, 2) > 200000:
            continue
        trials += 1
        exp = brute_force(side, pts, k)
        got = sol.maxDistance(side, [list(p) for p in pts], k)
        if got != exp:
            fails += 1
            print("MISMATCH side=%d k=%d got=%d exp=%d pts=%s" % (side, k, got, exp, pts))
            if fails > 5:
                break
    print("STRESS: trials=%d mismatches=%d -> %s (%.2fs)"
          % (trials, fails, "PASS" if fails == 0 else "FAIL", time.time() - t0))

    print("=== TIMING ===")
    SIDE = 10 ** 9
    N = 15000

    big = gen_random_boundary(SIDE, N, rng)
    for kk in (4, 12, 25):
        t0 = time.time()
        res = sol.maxDistance(SIDE, big, kk)
        print("random-boundary n=%d side=%d k=%d: ans=%d time=%.3fs"
              % (N, SIDE, kk, res, time.time() - t0))

    edge = gen_bottom_edge(SIDE, N, rng)
    for kk in (4, 25):
        t0 = time.time()
        res = sol.maxDistance(SIDE, edge, kk)
        print("single-edge n=%d side=%d k=%d: ans=%d time=%.3fs"
              % (N, SIDE, kk, res, time.time() - t0))


if __name__ == "__main__":
    main()