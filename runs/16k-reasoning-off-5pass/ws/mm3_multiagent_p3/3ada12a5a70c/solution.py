from typing import List
import itertools, random, bisect, sys

class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        """
        Exact solution: binary search on D combined with a backtracking feasibility
        check on the perimeter of the square.

        For any two boundary points of an axis‑aligned square the Manhattan distance
        equals the length of the shorter arc along the boundary, so the problem
        reduces to selecting k points on a circular line of length 4·side such that
        the minimum cyclic distance between any two chosen points is at least D.
        The feasibility test is exact because we try every possible first point and
        greedily place the next ones, with depth bounded by k (≤ 25).
        """
        n = len(points)
        perim = [0] * n
        for idx, (x, y) in enumerate(points):
            if y == 0:                # bottom edge
                perim[idx] = x
            elif x == side:           # right edge
                perim[idx] = side + y
            elif y == side:           # top edge
                perim[idx] = 2 * side + (side - x)
            else:                     # left edge (x == 0)
                perim[idx] = 3 * side + (side - y)

        # sort by perimeter coordinate
        perim_sorted = sorted(perim)
        P = 4 * side

        def feasible(D: int) -> bool:
            if D == 0:
                return True
            # duplicate to handle wrap‑around
            perim2 = perim_sorted + [p + P for p in perim_sorted]
            n2 = 2 * n
            # pre‑compute nxt2[i] = first index j > i with perim2[j] - perim2[i] >= D
            nxt2 = [n2] * n2
            j = 0
            for i in range(n2):
                while j < n2 and perim2[j] - perim2[i] < D:
                    j += 1
                nxt2[i] = j

            # backtracking: try every original point as the first selection
            def dfs(last_idx: int, remaining: int) -> bool:
                if remaining == 0:
                    return True
                idx = nxt2[last_idx]
                # we must pick exactly `remaining` more points
                while idx < n2 and n2 - idx >= remaining:
                    if dfs(idx, remaining - 1):
                        return True
                    # skip to the next candidate that is still >= D from last_idx
                    nxt_candidate = idx + 1
                    while nxt_candidate < n2 and perim2[nxt_candidate] - perim2[last_idx] < D:
                        nxt_candidate += 1
                    idx = nxt_candidate
                return False

            for first in range(n):
                if dfs(first, k - 1):
                    return True
            return False

        lo, hi = 0, 2 * side
        best = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                best = mid
                lo = mid + 1
            else:
                hi = mid - 1
        return best


# ---------------------- test harness ----------------------
def brute_max_min_distance(side, points, k):
    """Reference O(C(n,k)) brute force for tiny instances."""
    best = 0
    n = len(points)
    for combo in itertools.combinations(range(n), k):
        mn = float('inf')
        ok = True
        for i in range(k):
            for j in range(i + 1, k):
                a, b = points[combo[i]], points[combo[j]]
                d = abs(a[0] - b[0]) + abs(a[1] - b[1])
                if d < mn:
                    mn = d
        if mn > best:
            best = mn
    return best


def run_tests():
    sol = Solution()

    # Provided examples
    assert sol.maxDistance(2, [[0,2],[2,0],[2,2],[0,0]], 4) == 2, "Example 1 failed"
    assert sol.maxDistance(2, [[0,0],[1,2],[2,0],[2,2],[2,1]], 4) == 1, "Example 2 failed"
    assert sol.maxDistance(2, [[0,0],[0,1],[0,2],[1,2],[2,0],[2,2],[2,1]], 5) == 1, "Example 3 failed"

    # Random small cases vs brute force
    random.seed(0)
    for _ in range(50):
        side = random.randint(1, 6)
        # generate random points on boundary
        n = random.randint(4, 8)
        perim_set = set()
        pts = []
        while len(pts) < n:
            t = random.randint(0, 4 * side)
            if t in perim_set:
                continue
            perim_set.add(t)
            if t < side:
                x, y = t, 0
            elif t < 2 * side:
                x, y = side, t - side
            elif t < 3 * side:
                x, y = 3 * side - t, side
            else:
                x, y = 0, 4 * side - t
            pts.append([x, y])
        k = random.randint(4, min(6, n))
        ans = sol.maxDistance(side, pts, k)
        brute = brute_max_min_distance(side, pts, k)
        if ans != brute:
            print("MISMATCH", side, pts, k, "got", ans, "expected", brute)
            return
    print("All tests passed.")
    print("Example 1:", sol.maxDistance(2, [[0,2],[2,0],[2,2],[0,0]], 4))
    print("Example 2:", sol.maxDistance(2, [[0,0],[1,2],[2,0],[2,2],[2,1]], 4))
    print("Example 3:", sol.maxDistance(2, [[0,0],[0,1],[0,2],[1,2],[2,0],[2,2],[2,1]], 5))


if __name__ == "__main__":
    run_tests()