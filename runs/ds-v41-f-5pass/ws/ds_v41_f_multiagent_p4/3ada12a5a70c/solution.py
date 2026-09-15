from typing import List
from itertools import combinations
import random


class Solution:
    def maxDistance(self, side: int, points: List[List[int]], k: int) -> int:
        # Map each boundary point to a CCW perimeter coordinate in [0, 4*side).
        L = 4 * side
        coords = []
        for x, y in points:
            if y == 0:                      # bottom edge (x, 0)
                c = x
            elif x == side:                 # right edge (side, y)
                c = side + y
            elif y == side:                 # top edge (x, side)
                c = 2 * side + (side - x)
            else:                           # left edge (0, y)
                c = 3 * side + (side - y)
            coords.append(c)
        coords.sort()
        n = len(coords)

        # Doubled coordinates: a full lap is always indexable without modulo.
        pos2 = coords + [c + L for c in coords]
        m = 2 * n
        jumps = k - 1

        def feasible(D: int) -> bool:
            # nxt[i] = smallest j > i with pos2[j] - pos2[i] >= D (or m if none).
            nxt = [m] * m
            j = 0
            for i in range(m):
                if j <= i:
                    j = i + 1
                t = pos2[i] + D
                while j < m and pos2[j] < t:
                    j += 1
                nxt[i] = j

            # Try each point as the first (smallest) selected point.
            for i in range(n):
                idx = i
                limit = i + n          # staying below keeps the k points distinct
                for _ in range(jumps):
                    idx = nxt[idx]
                    if idx >= limit:
                        break
                else:
                    # closing (wrap-around) arc must also be >= D
                    if pos2[idx] - pos2[i] <= L - D:
                        return True
            return False

        lo, hi = 0, side
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


def _brute(side: int, points, k: int) -> int:
    best = 0
    for comb in combinations(points, k):
        md = min(abs(a[0] - b[0]) + abs(a[1] - b[1])
                 for a, b in combinations(comb, 2))
        if md > best:
            best = md
    return best


if __name__ == "__main__":
    sol = Solution()
    print(sol.maxDistance(2, [[0, 2], [2, 0], [2, 2], [0, 0]], 4))                     # 2
    print(sol.maxDistance(2, [[0, 0], [1, 2], [2, 0], [2, 2], [2, 1]], 4))             # 1
    print(sol.maxDistance(2, [[0, 0], [0, 1], [0, 2], [1, 2], [2, 0], [2, 2], [2, 1]], 5))  # 1

    random.seed(12345)
    mismatches = 0
    for _ in range(2000):
        s = random.randint(1, 6)
        bnd = []
        for x in range(s + 1):
            bnd.append((x, 0)); bnd.append((x, s))
        for y in range(1, s):
            bnd.append((0, y)); bnd.append((s, y))
        bnd = list(set(bnd))
        if len(bnd) < 4:
            continue
        n = random.randint(4, min(len(bnd), 8))
        pts = random.sample(bnd, n)
        for k in range(4, min(25, n) + 1):
            got = sol.maxDistance(s, [list(p) for p in pts], k)
            exp = _brute(s, [list(p) for p in pts], k)
            if got != exp:
                mismatches += 1
                print("MISMATCH", s, pts, k, "got", got, "exp", exp)
                if mismatches > 10:
                    break
        if mismatches > 10:
            break
    print("mismatches:", mismatches)