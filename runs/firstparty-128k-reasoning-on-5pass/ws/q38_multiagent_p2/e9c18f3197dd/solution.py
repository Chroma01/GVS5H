from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Remove duplicates and targets that divide another target.
        # If t divides u, any multiple of u is also a multiple of t.
        uniq = sorted(set(target))
        reduced = []
        for t in uniq:
            redundant = False
            for u in uniq:
                if u != t and u % t == 0:
                    redundant = True
                    break
            if not redundant:
                reduced.append(t)

        if not reduced:
            return 0
        if len(reduced) == 1 and reduced[0] == 1:
            return 0

        m = len(reduced)
        full = (1 << m) - 1

        # Valid upper bound: assign each remaining target to a distinct element.
        ub = sum(t - 1 for t in reduced)
        if ub == 0:
            return 0
        inf = ub + 1

        max_val = max(nums)
        limit = ub + max_val
        size = 1 << m

        # Precompute lcm for every target subset, capped when it can never be useful.
        lcm = [0] * size
        lcm[0] = 1
        for mask in range(1, size):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            l = lcm[prev]
            if l > limit:
                lcm[mask] = limit + 1
            else:
                t = reduced[i]
                g = gcd(l, t)
                l = (l // g) * t
                if l > limit:
                    l = limit + 1
                lcm[mask] = l

        # Split masks by whether their lcm is above the maximum original value.
        gt_max = []
        le_max = []
        for mask in range(1, size):
            L = lcm[mask]
            if L > limit:
                continue
            if L > max_val:
                gt_max.append((mask, L))
            else:
                le_max.append((mask, L))

        # Precompute transitions: for each already-covered mask, choose a nonempty
        # subset of still-uncovered targets for the current element.
        trans = [[] for _ in range(size)]
        for prev in range(size):
            comp = full ^ prev
            sub = comp
            while sub:
                trans[prev].append((sub, prev | sub))
                sub = (sub - 1) & comp

        dp = [inf] * size
        dp[0] = 0

        for v in nums:
            costs = [inf] * size

            for mask, L in gt_max:
                c = L - v
                if c <= ub:
                    costs[mask] = c

            for mask, L in le_max:
                r = v % L
                c = 0 if r == 0 else L - r
                if c <= ub:
                    costs[mask] = c

            new = dp.copy()
            for prev in range(size):
                base = dp[prev]
                if base >= inf:
                    continue
                for sub, nm in trans[prev]:
                    c = costs[sub]
                    if c < inf:
                        nc = base + c
                        if nc < new[nm]:
                            new[nm] = nc

            dp = new
            if dp[full] == 0:
                break

        return dp[full]


if __name__ == "__main__":
    import random

    sol = Solution()

    # Provided examples.
    assert sol.minimumIncrements([1, 2, 3], [4]) == 1
    assert sol.minimumIncrements([8, 4], [10, 5]) == 2
    assert sol.minimumIncrements([7, 9, 10], [7]) == 0

    # Edge cases.
    assert sol.minimumIncrements([1], [1]) == 0
    assert sol.minimumIncrements([1], [2]) == 1
    assert sol.minimumIncrements([1, 1], [2, 3]) == 3
    assert sol.minimumIncrements([5, 5], [2, 3]) == 1
    assert sol.minimumIncrements([1, 1, 1, 1], [2, 3, 4, 5]) == 9

    def brute(nums, target):
        targets = sorted(set(target))
        m = len(targets)
        if m == 0:
            return 0

        full = (1 << m) - 1
        size = 1 << m
        sub_lcm = [1] * size
        for mask in range(1, size):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            l = sub_lcm[prev]
            t = targets[i]
            g = gcd(l, t)
            sub_lcm[mask] = (l // g) * t

        best = 10 ** 9
        n = len(nums)

        def dfs(i, mask, cost):
            nonlocal best
            if cost >= best:
                return
            if i == n:
                if mask == full:
                    best = cost
                return

            comp = full ^ mask
            sub = comp
            while True:
                L = sub_lcm[sub]
                c = (L - nums[i] % L) % L
                dfs(i + 1, mask | sub, cost + c)
                if sub == 0:
                    break
                sub = (sub - 1) & comp

        dfs(0, 0, 0)
        return best

    # Tiny randomized cross-check.
    random.seed(12345)
    for _ in range(300):
        n = random.randint(1, 5)
        m = random.randint(1, min(4, n))
        nums = [random.randint(1, 12) for _ in range(n)]
        target = [random.randint(1, 12) for _ in range(m)]
        a = sol.minimumIncrements(nums, target)
        b = brute(nums, target)
        if a != b:
            raise AssertionError((nums, target, a, b))