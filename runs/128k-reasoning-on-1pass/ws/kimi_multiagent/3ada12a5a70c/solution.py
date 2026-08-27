from typing import List
from itertools import combinations
import random


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        L = 4 * side

        # Map each boundary point to a 1D perimeter coordinate t in [0, L),
        # walking counterclockwise starting at (0, 0).
        ts = []
        for x, y in points:
            if y == 0:            # bottom edge: (0,0) -> (side,0)
                t = x
            elif x == side:       # right edge:  (side,0) -> (side,side)
                t = side + y
            elif y == side:       # top edge:    (side,side) -> (0,side)
                t = 3 * side - x
            else:                 # left edge:   (0,side) -> (0,0)
                t = 4 * side - y
            ts.append(t % L)

        t = sorted(set(ts))
        n = len(t)
        # Duplicated array to handle circular wraparound.
        a = t + [v + L for v in t]  # length 2n, strictly increasing
        M = 2 * n

        def feasible(d: int) -> bool:
            # nxt[i] = smallest j > i with a[j] >= a[i] + d, else M (sentinel).
            nxt = [M] * M
            j = 0
            for i in range(M):
                if j < i + 1:
                    j = i + 1
                while j < M and a[j] - a[i] < d:
                    j += 1
                nxt[i] = j

            # Try every point as the start; greedily jump to the next
            # point at least d away, k - 1 times.
            for s in range(n):
                cur = s
                ok = True
                for _ in range(k - 1):
                    cur = nxt[cur]
                    if cur >= s + n:  # passed the copy of the start / sentinel
                        ok = False
                        break
                if not ok:
                    continue
                # Wraparound gap from last selected point back to start.
                if a[s] + L - a[cur] >= d:
                    return True
            return False

        # For k >= 4, L // k <= side, and in the regime d <= side the
        # Manhattan distance on the boundary matches the circular perimeter
        # distance (opposite-side pairs are automatically >= side >= d).
        lo, hi = 0, min(side, L // k)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


# ---------------------------------------------------------------------------
# Stress-test harness
# ---------------------------------------------------------------------------

def brute_force(side: int, points, k: int) -> int:
    """Exact answer by enumerating all k-subsets (true Manhattan metric)."""
    best = 0
    idx = range(len(points))
    for combo in combinations(idx, k):
        mn = None
        for i, j in combinations(combo, 2):
            d = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
            if mn is None or d < mn:
                mn = d
        if mn > best:
            best = mn
    return best


def boundary_points(side: int):
    """All lattice points on the boundary of the side x side square."""
    pts = set()
    for x in range(side + 1):
        pts.add((x, 0))
        pts.add((x, side))
    for y in range(1, side):
        pts.add((0, y))
        pts.add((side, y))
    return sorted(pts)


def check(side, pts, k, failures, label):
    pts_list = [list(p) for p in pts]
    got = Solution().maxDistance(side, pts_list, k)
    exp = brute_force(side, pts, k)
    if got != exp:
        failures.append((label, side, pts, k, exp, got))
        print(f"MISMATCH [{label}] side={side} k={k} points={pts} "
              f"expected={exp} got={got}")
        return False
    return True


def run_stress():
    rng = random.Random(12345)
    failures = []
    total = 0

    # 1) Exhaustive over ALL subsets and ALL valid k for side = 2.
    for side in (2,):
        allp = boundary_points(side)
        for r in range(4, len(allp) + 1):
            for sub in combinations(allp, r):
                for k in range(4, r + 1):
                    total += 1
                    check(side, list(sub), k, failures, "exhaustive")

    # 2) Random subsets / random k for side = 2, 3, 4.
    for side in (2, 3, 4):
        allp = boundary_points(side)
        for _ in range(400):
            n = rng.randint(4, len(allp))
            pts = rng.sample(allp, n)
            k = rng.randint(4, n)
            total += 1
            check(side, pts, k, failures, "random")

    # 3) Directed opposite-side midpoint cases: pairs where the short
    #    perimeter arc differs from the Manhattan distance, e.g.
    #    (0, y) vs (side, side - y) with y < side/2 (arc > Manhattan)
    #    and (x, 0) vs (side - x, side) (top/bottom counterparts).
    for side in (2, 3, 4):
        allp = boundary_points(side)
        mid_pairs = []
        for y in range(0, side // 2 + 1):
            mid_pairs.append(((0, y), (side, side - y)))       # left vs right
            mid_pairs.append(((y, 0), (side - y, side)))       # bottom vs top
            mid_pairs.append(((0, side - y), (side, y)))
            mid_pairs.append(((side - y, 0), (y, side)))
        for rep in range(60):
            pts = set()
            # Force 1..3 arc-vs-Manhattan divergent opposite pairs in.
            for (p, q) in rng.sample(mid_pairs, rng.randint(1, 3)):
                pts.add(p)
                pts.add(q)
            # Fill with random other boundary points.
            while len(pts) < rng.randint(4, len(allp)):
                pts.add(rng.choice(allp))
            pts = sorted(pts)
            if len(pts) < 4:
                continue
            for k in range(4, len(pts) + 1):
                total += 1
                check(side, pts, k, failures, "opposite-midpoints")

    # 4) Worst-case k = 4 with exactly one point forced on each side
    #    (regime boundary d close to side).
    for side in (2, 3, 4):
        for _ in range(300):
            pts = {
                (rng.randint(0, side), 0),
                (rng.randint(0, side), side),
                (0, rng.randint(0, side)),
                (side, rng.randint(0, side)),
            }
            if len(pts) < 4:
                continue
            pts = sorted(pts)
            total += 1
            check(side, pts, 4, failures, "one-per-side")

    # 5) Provided examples as sanity checks.
    examples = [
        (2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4, 2),
        (2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4, 1),
        (2, [[0, 0], [0, 1], [0, 2], [1, 2], [2, 0], [2, 2], [2, 1]], 5, 1),
    ]
    for side, pts, k, exp in examples:
        got = Solution().maxDistance(side, pts, k)
        total += 1
        if got != exp:
            failures.append(("example", side, pts, k, exp, got))
            print(f"MISMATCH [example] side={side} k={k} expected={exp} got={got}")

    print(f"\nRan {total} stress tests.")
    if failures:
        print(f"FAILED: {len(failures)} mismatch(es) found.")
        raise SystemExit(1)
    print("ALL PASSED: solution matches brute force everywhere.")


if __name__ == "__main__":
    run_stress()