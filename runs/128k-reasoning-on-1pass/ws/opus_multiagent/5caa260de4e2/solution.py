from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # prefix sums
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for idx in range(n):
            P[idx + 1] = P[idx] + nums[idx]
            C[idx + 1] = C[idx] + cost[idx]

        Cn = C[n]
        kCn = k * Cn

        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0

        for j in range(1, n + 1):
            Pj = P[j]
            Cj = C[j]
            base = Pj * Cj + kCn
            x = Pj + k
            best = INF
            for i in range(j):
                v = dp[i] - C[i] * x
                if v < best:
                    best = v
            dp[j] = base + best

        return dp[n]


if __name__ == "__main__":
    s = Solution()
    assert s.minimumCost([3, 1, 4], [4, 6, 6], 1) == 110, s.minimumCost([3, 1, 4], [4, 6, 6], 1)
    r2 = s.minimumCost([4, 8, 5, 1, 14, 2, 2, 12, 1], [7, 2, 8, 4, 2, 2, 1, 1, 2], 7)
    assert r2 == 985, r2

    # brute force validation
    import random
    from itertools import product

    def brute(nums, cost, k):
        n = len(nums)
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]
        best = float('inf')
        for mask in product([0, 1], repeat=max(n - 1, 0)):
            cuts = [i + 1 for i, b in enumerate(mask) if b]
            bounds = [0] + cuts + [n]
            total = 0
            for t in range(1, len(bounds)):
                l, r = bounds[t - 1], bounds[t]
                total += (P[r] + k * t) * (C[r] - C[l])
            best = min(best, total)
        return best

    random.seed(1)
    for _ in range(300):
        n = random.randint(1, 8)
        nums = [random.randint(1, 10) for _ in range(n)]
        cost = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(1, 10)
        a = s.minimumCost(nums, cost, k)
        b = brute(nums, cost, k)
        assert a == b, (nums, cost, k, a, b)
    print("all tests passed")