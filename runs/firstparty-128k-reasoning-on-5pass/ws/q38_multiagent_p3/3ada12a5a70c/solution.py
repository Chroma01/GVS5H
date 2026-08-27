from typing import List
from itertools import combinations


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        C = 4 * side

        def perimeter_coord(pt: List[int]) -> int:
            x, y = pt
            if y == 0:
                return x
            if x == side:
                return side + y
            if y == side:
                return 3 * side - x
            return 4 * side - y

        p = sorted(perimeter_coord(pt) for pt in points)
        n = len(p)
        p2 = p + [x + C for x in p]
        nxt = [0] * (2 * n)
        all_indices = range(2 * n)
        starts = range(n)
        jump_range = range(k - 1)

        def can(D: int) -> bool:
            if D == 0:
                return True

            pp = p2
            nn = n
            mm = 2 * nn
            CC = C
            nnxt = nxt
            all_idx = all_indices
            st = starts
            jr = jump_range

            j = 1
            for i in all_idx:
                if j <= i:
                    j = i + 1
                target = pp[i] + D
                while j < mm and pp[j] < target:
                    j += 1
                nnxt[i] = j

            for s in st:
                idx = s
                limit = s + nn
                for _ in jr:
                    idx = nnxt[idx]
                    if idx >= limit:
                        break
                else:
                    if pp[s] + CC - pp[idx] >= D:
                        return True
            return False

        lo, hi = 0, min(side, C // k)
        ans = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if can(mid):
                ans = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return ans


def _boundary_points(side: int) -> List[List[int]]:
    pts: List[List[int]] = []
    for x in range(side + 1):
        pts.append([x, 0])
        pts.append([x, side])
    for y in range(1, side):
        pts.append([0, y])
        pts.append([side, y])
    return pts


def _brute_force(points: List[List[int]], k: int) -> int:
    n = len(points)
    if k <= 1:
        return 0

    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            d = abs(xi - xj) + abs(yi - yj)
            dist[i][j] = d
            dist[j][i] = d

    best = 0
    for comb in combinations(range(n), k):
        md = 10**18
        for a in range(k - 1):
            ia = comb[a]
            dia = dist[ia]
            for b in range(a + 1, k):
                d = dia[comb[b]]
                if d < md:
                    if d <= best:
                        md = d
                        break
                    md = d
            if md <= best:
                break
        if md > best:
            best = md
    return best


def _run_self_tests() -> None:
    from random import Random

    sol = Solution()

    assert sol.maxDistance(2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4) == 2
    assert sol.maxDistance(2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4) == 1
    assert sol.maxDistance(2, [[0, 0], [0, 1], [0, 2], [1, 2], [2, 0], [2, 2], [2, 1]], 5) == 1

    # Exhaustive cross-check for all subsets of the small side=1 and side=2 squares.
    for side in (1, 2):
        all_pts = _boundary_points(side)
        total = len(all_pts)
        for mask in range(1, 1 << total):
            pts = [all_pts[i] for i in range(total) if mask & (1 << i)]
            n = len(pts)
            if n < 4:
                continue
            for k in range(4, n + 1):
                expected = _brute_force(pts, k)
                got = sol.maxDistance(side, pts, k)
                if got != expected:
                    raise AssertionError(
                        f"side={side} mask={mask} k={k}: got {got}, expected {expected}"
                    )

    # Full boundary sets for side 1..4.
    for side in range(1, 5):
        pts = _boundary_points(side)
        n = len(pts)
        for k in {4, n}:
            if 4 <= k <= n:
                expected = _brute_force(pts, k)
                got = sol.maxDistance(side, pts, k)
                if got != expected:
                    raise AssertionError(
                        f"full side={side} k={k}: got {got}, expected {expected}"
                    )

    # Deterministic random cross-check for side <= 4.
    rng = Random(20240525)
    for _ in range(30):
        side = rng.randint(1, 4)
        all_pts = _boundary_points(side)
        n = rng.randint(4, len(all_pts))
        pts = rng.sample(all_pts, n)
        k = rng.randint(4, min(n, 25))

        expected = _brute_force(pts, k)
        got = sol.maxDistance(side, pts, k)
        if got != expected:
            raise AssertionError(
                f"side={side} k={k} pts={pts} got={got} expected={expected}"
            )


if __name__ == "__main__":
    _run_self_tests()