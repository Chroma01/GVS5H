from typing import List
from itertools import combinations


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums: N[r] = nums[0..r], C[r] = cost[0..r]
        N = [0] * n
        C = [0] * n
        s = 0
        for i, v in enumerate(nums):
            s += v
            N[i] = s
        s = 0
        for i, v in enumerate(cost):
            s += v
            C[i] = s
        TC = C[n - 1]

        INF = float('inf')
        # f[r] = min total (excluding the constant k*TC) for nums[0..r]
        # f[r] = min_{p in [-1, r-1]} f[p] + N[r]*(C[r]-C[p])
        #        + (k*(TC - C[p]) if p >= 0 else 0)
        f = [0] * n
        for r in range(n):
            best = N[r] * C[r]  # p = -1: single segment, no cut penalty
            Nr = N[r]
            Cr = C[r]
            for p in range(r):
                cand = f[p] + Nr * (Cr - C[p]) + k * (TC - C[p])
                if cand < best:
                    best = cand
            f[r] = best

        return f[n - 1] + k * TC


# ---------------- validation ----------------

def brute_force(nums, cost, k):
    """Directly enumerate all partitions and compute cost per statement."""
    n = len(nums)
    N = [0] * n
    s = 0
    for i, v in enumerate(nums):
        s += v
        N[i] = s

    best = None
    # choose subset of cut positions among 0..n-2 (cut after index p)
    for mask in range(1 << (n - 1)):
        cuts = [p for p in range(n - 1) if mask >> p & 1]
        bounds = [-1] + cuts + [n - 1]
        total = 0
        for i in range(1, len(bounds)):
            l, r = bounds[i - 1] + 1, bounds[i]
            csum = sum(cost[l:r + 1])
            total += (N[r] + k * i) * csum
        if best is None or total < best:
            best = total
    return best


if __name__ == "__main__":
    sol = Solution()

    # Provided examples
    assert sol.minimumCost([3, 1, 4], [4, 6, 6], 1) == 110
    assert sol.minimumCost([4, 8, 5, 1, 14, 2, 2, 12, 1],
                           [7, 2, 8, 4, 2, 2, 1, 1, 2], 7) == 985

    # Random small tests vs brute force
    import random
    random.seed(0)
    for _ in range(300):
        n = random.randint(1, 8)
        nums = [random.randint(1, 10) for _ in range(n)]
        cost = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(1, 10)
        got = sol.minimumCost(nums, cost, k)
        exp = brute_force(nums, cost, k)
        assert got == exp, (nums, cost, k, got, exp)

    print("All tests passed.")