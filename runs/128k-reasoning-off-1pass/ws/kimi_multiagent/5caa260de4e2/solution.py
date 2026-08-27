import sys
from collections import deque
from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums (1-based): S[i] = sum(nums[0..i-1]), C[i] = sum(cost[0..i-1])
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float('inf')

        # dp_prev[i] = min cost to partition first i elements (nums[0..i-1])
        # using (j-1) subarrays. dp_cur[i] = same but with j subarrays.
        # Transition (i >= 1, j >= 1):
        #   dp_cur[i] = min over l in [j-1 .. i-1] of
        #       dp_prev[l] + (S[i] + k*j) * (C[i] - C[l])
        #             = (S[i] + k*j) * C[i]
        #               + min over l of ( dp_prev[l] - (S[i] + k*j) * C[l] )
        # For fixed j, each l defines a line f_l(x) = dp_prev[l] - C[l] * x,
        # queried at x = S[i] + k*j.
        # Slopes m = -C[l] are non-increasing as l grows (C non-decreasing),
        # and query x is non-decreasing as i grows (S non-decreasing),
        # so a monotone convex hull trick with a deque gives O(n) per j.

        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0  # empty prefix, 0 subarrays

        answer = INF
        for j in range(1, n + 1):
            kj = k * j
            dp_cur = [INF] * (n + 1)
            # Hull stores lines (m, b): f(x) = m*x + b, slopes decreasing.
            hull = deque()

            def bad(l1, l2, l3):
                # True if l2 is unnecessary (for min query, slopes decreasing)
                # intersection(l1, l3) <= intersection(l1, l2)
                # (b3 - b1)/(m1 - m3) <= (b2 - b1)/(m1 - m2)
                # cross-multiply (denominators >= 0 since m1 >= m2 >= m3):
                return (l3[1] - l1[1]) * (l1[0] - l2[0]) <= \
                       (l2[1] - l1[1]) * (l1[0] - l3[0])

            # l ranges from j-1 to i-1; we add line for l = i-1 before query i.
            # Start: line for l = j-1 must exist before querying i = j.
            # We'll add lines incrementally.
            next_l = j - 1
            for i in range(j, n + 1):
                # Add line for l = i - 1 (if not added yet)
                while next_l <= i - 1:
                    l = next_l
                    if dp_prev[l] < INF:
                        m = -C[l]
                        b = dp_prev[l]
                        new_line = (m, b)
                        while len(hull) >= 2 and bad(hull[-2], hull[-1], new_line):
                            hull.pop()
                        # If same slope as last, keep the one with smaller b
                        if hull and hull[-1][0] == m:
                            if hull[-1][1] <= b:
                                pass  # existing line is better everywhere
                                next_l += 1
                                continue
                            else:
                                hull.pop()
                        hull.append(new_line)
                    next_l += 1

                x = S[i] + kj
                # Query min at x; pop front while next line is better
                while len(hull) >= 2 and \
                        hull[0][0] * x + hull[0][1] >= hull[1][0] * x + hull[1][1]:
                    hull.popleft()
                best = hull[0][0] * x + hull[0][1]
                dp_cur[i] = (S[i] + kj) * C[i] + best

            if dp_cur[n] < answer:
                answer = dp_cur[n]
            dp_prev = dp_cur

        return answer


# ---------------- Brute force reference (O(n^3)) ----------------
def brute_force(nums, cost, k):
    n = len(nums)
    S = [0] * (n + 1)
    C = [0] * (n + 1)
    for i in range(n):
        S[i + 1] = S[i] + nums[i]
        C[i + 1] = C[i] + cost[i]
    INF = float('inf')
    # dp[j][i]: first i elements in j subarrays
    dp = [[INF] * (n + 1) for _ in range(n + 1)]
    dp[0][0] = 0
    for j in range(1, n + 1):
        for i in range(j, n + 1):
            best = INF
            for l in range(j - 1, i):
                if dp[j - 1][l] < INF:
                    v = dp[j - 1][l] + (S[i] + k * j) * (C[i] - C[l])
                    if v < best:
                        best = v
            dp[j][i] = best
    return min(dp[j][n] for j in range(1, n + 1))


def _run_tests():
    sol = Solution()
    # Given examples
    assert sol.minimumCost([3, 1, 4], [4, 6, 6], 1) == 110
    assert sol.minimumCost([4, 8, 5, 1, 14, 2, 2, 12, 1],
                           [7, 2, 8, 4, 2, 2, 1, 1, 2], 7) == 985
    # Edge cases
    assert sol.minimumCost([1], [1], 1) == (1 + 1) * 1  # single element
    assert sol.minimumCost([5], [3], 10) == (5 + 10) * 3
    # Cross-validate with brute force on random small inputs
    import random
    random.seed(12345)
    for _ in range(300):
        n = random.randint(1, 9)
        nums = [random.randint(1, 10) for _ in range(n)]
        cost = [random.randint(1, 10) for _ in range(n)]
        k = random.randint(1, 10)
        got = sol.minimumCost(nums, cost, k)
        exp = brute_force(nums, cost, k)
        assert got == exp, (nums, cost, k, got, exp)
    print("All tests passed.")


if __name__ == "__main__":
    _run_tests()