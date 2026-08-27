from typing import List
import random

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        Tn = C[n]
        INF = 10**30
        dp = [INF] * (n + 1)
        dp[0] = 0
        kTn = k * Tn

        for b in range(1, n + 1):
            Sb = S[b]
            best = INF
            for a in range(b):
                val = dp[a] + kTn + C[a] * (S[a] - Sb - k)
                if val < best:
                    best = val
            dp[b] = best

        return dp[n] + S[n] * C[n]


def brute_force(nums: List[int], cost: List[int], k: int) -> int:
    n = len(nums)
    S = [0] * (n + 1)
    C = [0] * (n + 1)
    for i in range(n):
        S[i + 1] = S[i] + nums[i]
        C[i + 1] = C[i] + cost[i]

    best = 10**30

    def dfs(pos: int, parts: int, total: int) -> None:
        nonlocal best
        if total >= best:
            return
        if pos == n:
            best = total
            return
        for r in range(pos, n):
            add = (S[r + 1] + k * (parts + 1)) * (C[r + 1] - C[pos])
            dfs(r + 1, parts + 1, total + add)

    dfs(0, 0, 0)
    return best


if __name__ == "__main__":
    sol = Solution()

    assert sol.minimumCost([3, 1, 4], [4, 6, 6], 1) == 110
    assert brute_force([3, 1, 4], [4, 6, 6], 1) == 110

    assert sol.minimumCost([4, 8, 5, 1, 14, 2, 2, 12, 1],
                           [7, 2, 8, 4, 2, 2, 1, 1, 2], 7) == 985
    assert brute_force([4, 8, 5, 1, 14, 2, 2, 12, 1],
                       [7, 2, 8, 4, 2, 2, 1, 1, 2], 7) == 985

    random.seed(2024)
    for _ in range(1000):
        n = random.randint(1, 10)
        nums = [random.randint(1, 10) for _ in range(n)]
        cost = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(1, 10)

        expected = brute_force(nums, cost, k)
        got = sol.minimumCost(nums, cost, k)

        if expected != got:
            print("Mismatch", nums, cost, k, expected, got)
            raise AssertionError

    sol.minimumCost([1000] * 1000, [1000] * 1000, 1000)
    print("All tests passed")