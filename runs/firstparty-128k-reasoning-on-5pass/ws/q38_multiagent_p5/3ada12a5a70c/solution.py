from typing import List


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        if k <= 1:
            return 0

        # Not needed for the stated constraints (k >= 4), but keeps the method
        # correct for the trivial k == 2 case.
        if k == 2:
            if not points:
                return 0
            it = iter(points)
            x0, y0 = next(it)
            max_sum = min_sum = x0 + y0
            max_diff = min_diff = x0 - y0
            for x, y in it:
                s = x + y
                if s > max_sum:
                    max_sum = s
                elif s < min_sum:
                    min_sum = s

                d = x - y
                if d > max_diff:
                    max_diff = d
                elif d < min_diff:
                    min_diff = d

            return max(max_sum - min_sum, max_diff - min_diff)

        C = 4 * side

        # Perimeter coordinate in [0, 4*side).
        # The if-order assigns corners consistently:
        # (0,0) -> 0, (side,0) -> side, (side,side) -> 2*side, (0,side) -> 3*side.
        p = []
        for x, y in points:
            if y == 0:
                p.append(x)
            elif x == side:
                p.append(side + y)
            elif y == side:
                p.append(3 * side - x)
            else:  # x == 0
                p.append(4 * side - y)

        p.sort()
        n = len(p)
        if k > n:
            return 0

        p2 = p + [v + C for v in p]
        m = 2 * n

        def feasible(D: int) -> bool:
            if D == 0:
                return True

            # The k clockwise gaps around the perimeter sum to C.
            if k * D > C:
                return False

            # next[i] = first index j with p2[j] >= p2[i] + D.
            nxt = [0] * m
            j = 0
            p2_local = p2
            for i in range(m):
                if j < i:
                    j = i
                target = p2_local[i] + D
                while j < m and p2_local[j] < target:
                    j += 1
                nxt[i] = j

            need = k - 1
            wrap = C - D
            jump_range = range(need)
            p_local = p
            nxt_local = nxt

            for i in range(n):
                cur = i
                limit = i + n

                for _ in jump_range:
                    cur = nxt_local[cur]
                    if cur >= limit:
                        break
                else:
                    # Wrap gap from cur back to i + C is at least D.
                    if p2_local[cur] <= p_local[i] + wrap:
                        return True

            return False

        # For k >= 4, the answer is at most side.
        lo, hi = 0, side
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1

        return lo


def _run_tests() -> None:
    from itertools import combinations
    import random

    def boundary_points(side: int):
        pts = []
        for x in range(side + 1):
            pts.append((x, 0))
        for y in range(1, side + 1):
            pts.append((side, y))
        for x in range(side - 1, -1, -1):
            pts.append((x, side))
        for y in range(side - 1, 0, -1):
            pts.append((0, y))
        return pts

    def brute_force(points, k: int) -> int:
        best = 0
        for comb in combinations(points, k):
            mn = 10**18
            for i in range(k):
                x1, y1 = comb[i]
                for j in range(i + 1, k):
                    x2, y2 = comb[j]
                    d = abs(x1 - x2) + abs(y1 - y2)
                    if d < mn:
                        mn = d
            if mn > best:
                best = mn
        return best

    sol = Solution()

    # Provided examples.
    assert sol.maxDistance(2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4) == 2
    assert sol.maxDistance(2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4) == 1
    assert sol.maxDistance(
        2,
        [[0, 0], [0, 1], [0, 2], [1, 2], [2, 0], [2, 2], [2, 1]],
        5,
    ) == 1

    # Random brute-force validation on small squares.
    random.seed(2024)
    for _ in range(200):
        side = random.randint(1, 4)
        all_pts = boundary_points(side)
        n = random.randint(4, min(len(all_pts), 10))
        pts = random.sample(all_pts, n)
        k = random.randint(4, min(n, 6))

        expected = brute_force(pts, k)
        got = sol.maxDistance(side, pts, k)

        if expected != got:
            print("Mismatch:", side, pts, k, "expected", expected, "got", got)
            raise AssertionError("Random validation failed")


if __name__ == "__main__":
    _run_tests()