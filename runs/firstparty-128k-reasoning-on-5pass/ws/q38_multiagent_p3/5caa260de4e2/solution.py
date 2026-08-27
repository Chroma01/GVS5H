from typing import List
import random


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Q[i] = sum of cost[0..i-1]
        q = [0] * (n + 1)
        for i, c in enumerate(cost):
            q[i + 1] = q[i] + c
        total_cost = q[n]

        # Constant part:
        # sum over each element b of cost[b] * (nums[0] + ... + nums[b])
        constant = 0
        pref_num = 0
        for x, c in zip(nums, cost):
            pref_num += x
            constant += c * pref_num

        INF = 10 ** 30
        dp = [INF] * (n + 1)
        dp[0] = 0

        # dp[i] = minimum extra cost for prefix nums[0..i-1], where extra cost
        # consists of:
        #   1. internal pair costs: nums[a] * cost[b] for b < a in same segment
        #   2. cut penalties: for a cut after j elements, k * (Q[n] - Q[j])
        for j in range(n):
            base = dp[j]
            if base >= INF:
                continue

            # If j > 0, starting a new segment at j means placing a cut at j.
            if j > 0:
                base += k * (total_cost - q[j])

            pair = 0
            qj = q[j]

            # Extend the last segment from j to i-1.
            # When adding element a = i-1, it forms new internal pairs with
            # all previous elements b in [j, a-1], contributing:
            # nums[a] * (cost[j] + ... + cost[a-1])
            for i in range(j + 1, n + 1):
                pair += nums[i - 1] * (q[i - 1] - qj)
                val = base + pair
                if val < dp[i]:
                    dp[i] = val

        return constant + k * total_cost + dp[n]


def brute_force(nums: List[int], cost: List[int], k: int) -> int:
    """Direct enumeration of all partitions for tiny n."""
    n = len(nums)
    if n == 0:
        return 0

    p = [0] * (n + 1)
    q = [0] * (n + 1)
    for i in range(n):
        p[i + 1] = p[i] + nums[i]
        q[i + 1] = q[i] + cost[i]

    best = 10 ** 30

    # Bit i is 1 if there is a cut after element i (0-indexed), for i in [0, n-2].
    for mask in range(1 << (n - 1)):
        total = 0
        seg = 1
        start = 0

        for i in range(n - 1):
            if (mask >> i) & 1:
                end = i
                total += (p[end + 1] + k * seg) * (q[end + 1] - q[start])
                seg += 1
                start = end + 1

        total += (p[n] + k * seg) * (q[n] - q[start])
        if total < best:
            best = total

    return best


if __name__ == "__main__":
    sol = Solution()

    # Given examples.
    assert sol.minimumCost([3, 1, 4], [4, 6, 6], 1) == 110
    assert sol.minimumCost(
        [4, 8, 5, 1, 14, 2, 2, 12, 1],
        [7, 2, 8, 4, 2, 2, 1, 1, 2],
        7
    ) == 985

    # Edge cases.
    assert sol.minimumCost([1], [1], 1) == 2
    assert sol.minimumCost([1000], [1000], 1000) == 2000000
    assert sol.minimumCost([1, 1], [1, 1], 1) == 6
    assert sol.minimumCost([1, 2], [3, 4], 5) == brute_force([1, 2], [3, 4], 5)

    # Random tiny tests against brute force.
    random.seed(2024)
    for _ in range(300):
        n = random.randint(1, 9)
        nums = [random.randint(1, 6) for _ in range(n)]
        cost = [random.randint(1, 6) for _ in range(n)]
        k = random.randint(1, 6)

        expected = brute_force(nums, cost, k)
        got = sol.minimumCost(nums, cost, k)
        assert got == expected, (nums, cost, k, got, expected)