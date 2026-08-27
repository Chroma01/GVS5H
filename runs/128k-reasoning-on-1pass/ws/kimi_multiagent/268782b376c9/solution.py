from typing import List
from collections import deque
from itertools import product
import random


class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)

        def feasible(target: int) -> bool:
            if target <= 0:
                return True
            if m < n:
                return False
            need = [(target + p - 1) // p for p in points]
            return min_moves_formula(need) <= m

        lo, hi = 0, max(points) * m
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if feasible(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo


def min_moves_formula(need: List[int]) -> int:
    """
    Minimum moves, starting from -1, to visit index i at least need[i] times.
    Valid for the problem constraints n >= 2 and need[i] >= 1.
    """
    n = len(need)
    if n == 0:
        return 0
    if n == 1:
        # Outside the given constraints; with one cell only the forced first move exists.
        return 1 if need[0] <= 1 else 10**30

    a = need[:]                 # undiscounted demands
    b = [x - 1 for x in need]   # discounted demands for vertices <= end

    # left_b[i] = MWIS weight on b[0..i]
    left_b = [0] * n
    dp2 = dp1 = 0  # dp[i-2], dp[i-1]
    for i, w in enumerate(b):
        cur = max(dp1, dp2 + w)
        left_b[i] = cur
        dp2, dp1 = dp1, cur

    # right_a[i] = MWIS weight on a[i..n-1]
    right_a = [0] * n
    dp1 = dp2 = 0  # suffix i+1, suffix i+2
    for i in range(n - 1, -1, -1):
        cur = max(dp1, dp2 + a[i])
        right_a[i] = cur
        dp2, dp1 = dp1, cur

    best = 10**30
    for e in range(n):
        # MWIS either does not take e, or takes e and excludes e-1/e+1.
        not_take = (left_b[e - 1] if e - 1 >= 0 else 0) + \
                   (right_a[e + 1] if e + 1 < n else 0)
        take = (left_b[e - 2] if e - 2 >= 0 else 0) + b[e] + \
               (right_a[e + 2] if e + 2 < n else 0)
        mwis = max(not_take, take)
        best = min(best, e + 1 + 2 * mwis)
    return best


def min_moves_bruteforce(need: List[int], limit: int = 200):
    """BFS over (position, capped visit counts) for tiny validation cases."""
    n = len(need)
    target = tuple(need)
    start_counts = tuple([0] * n)
    if start_counts == target:
        return 0

    seen = {(-1, start_counts)}
    q = deque([(-1, start_counts, 0)])

    while q:
        pos, counts, dist = q.popleft()
        if counts == target:
            return dist
        if dist >= limit:
            continue

        if pos == -1:
            nxts = [0]
        else:
            nxts = []
            if pos > 0:
                nxts.append(pos - 1)
            if pos + 1 < n:
                nxts.append(pos + 1)

        for nxt in nxts:
            c = list(counts)
            if c[nxt] < need[nxt]:
                c[nxt] += 1
            c = tuple(c)
            state = (nxt, c)
            if state not in seen:
                seen.add(state)
                q.append((nxt, c, dist + 1))
    return None


def validate_formula() -> None:
    # Exhaustive tiny cases.
    for n in range(2, 5):
        for need in product(range(1, 4), repeat=n):
            need = list(need)
            f = min_moves_formula(need)
            b = min_moves_bruteforce(need, limit=100)
            assert b is not None and f == b, (need, f, b)

    # Random tiny cases.
    rng = random.Random(123456789)
    for _ in range(500):
        n = rng.randint(2, 4)
        need = [rng.randint(1, 5) for _ in range(n)]
        f = min_moves_formula(need)
        b = min_moves_bruteforce(need, limit=120)
        assert b is not None and f == b, (need, f, b)

    print("formula validation passed")


if __name__ == "__main__":
    validate_formula()
    print(Solution().maxScore([2, 4], 3))      # 4
    print(Solution().maxScore([1, 2, 3], 5))   # 2