from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        total_cost = C[n]
        k_total_cost = k * total_cost

        INF = 10**30
        dp = [INF] * (n + 1)
        dp[0] = 0

        for v in range(1, n + 1):
            Pv = P[v]
            best = INF
            for u in range(v):
                val = dp[u] + k_total_cost - C[u] * (Pv - P[u] + k)
                if val < best:
                    best = val
            dp[v] = best

        return P[n] * C[n] + dp[n]


def _brute_force(nums: List[int], cost: List[int], k: int) -> int:
    n = len(nums)

    P = [0] * (n + 1)
    C = [0] * (n + 1)
    for i in range(n):
        P[i + 1] = P[i] + nums[i]
        C[i + 1] = C[i] + cost[i]

    best = 10**30

    for mask in range(1 << (n - 1)):
        total = 0
        prev = 0
        seg = 1

        for i in range(n - 1):
            if mask & (1 << i):
                end = i + 1
                total += (P[end] + k * seg) * (C[end] - C[prev])
                prev = end
                seg += 1

        total += (P[n] + k * seg) * (C[n] - C[prev])

        if total < best:
            best = total

    return best


if __name__ == "__main__":
    sol = Solution()

    assert sol.minimumCost([3, 1, 4], [4, 6, 6], 1) == 110
    assert sol.minimumCost(
        [4, 8, 5, 1, 14, 2, 2, 12, 1],
        [7, 2, 8, 4, 2, 2, 1, 1, 2],
        7
    ) == 985

    import random
    random.seed(2024)

    for _ in range(200):
        n = random.randint(1, 8)
        nums = [random.randint(1, 10) for _ in range(n)]
        cost = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(1, 10)

        expected = _brute_force(nums, cost, k)
        got = sol.minimumCost(nums, cost, k)

        if expected != got:
            print("Mismatch:", nums, cost, k, expected, got)
            raise SystemExit(1)

    print("All self-tests passed.")