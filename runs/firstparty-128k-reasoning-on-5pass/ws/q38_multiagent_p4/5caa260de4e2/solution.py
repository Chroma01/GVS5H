from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # P[i] = sum(nums[0..i-1])
        # Q[i] = sum(cost[0..i-1])
        P = [0] * (n + 1)
        Q = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            Q[i + 1] = Q[i] + cost[i]

        total_cost = Q[n]

        # dp[i] = minimum cost for prefix 0..i-1, counting:
        #   - all non-k segment contributions
        #   - penalties for internal cuts strictly before i
        # The final endpoint i is not penalized yet.
        dp = [0] * (n + 1)

        for i in range(1, n + 1):
            Pi = P[i]
            Qi = Q[i]

            # Previous cut p = 0: no cut penalty.
            best = Pi * Qi

            # Previous cut p > 0: p becomes an internal cut,
            # so add its fixed penalty k * (total_cost - Q[p]).
            for p in range(1, i):
                val = dp[p] + Pi * (Qi - Q[p]) + k * (total_cost - Q[p])
                if val < best:
                    best = val

            dp[i] = best

        # Every partition has a base k * total_cost contribution.
        return dp[n] + k * total_cost


if __name__ == "__main__":
    sol = Solution()

    ans1 = sol.minimumCost([3, 1, 4], [4, 6, 6], 1)
    ans2 = sol.minimumCost(
        [4, 8, 5, 1, 14, 2, 2, 12, 1],
        [7, 2, 8, 4, 2, 2, 1, 1, 2],
        7
    )
    ans3 = sol.minimumCost([5], [2], 3)

    print(ans1)
    print(ans2)
    print(ans3)

    assert ans1 == 110
    assert ans2 == 985
    assert ans3 == 16