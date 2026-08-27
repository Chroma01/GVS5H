from typing import List
from collections import deque

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float('inf')
        # dp_prev[j] = min cost to partition first j elements into (g-1) groups
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0  # 0 elements, 0 groups, cost 0

        ans = INF

        for g in range(1, n + 1):
            dp_curr = [INF] * (n + 1)
            # Convex hull for lines y = m*x + b
            # m = -C[j], b = dp_prev[j]
            # Slopes are non-increasing (since C[j] is non-decreasing)
            # Queries x = S[i] + k*g are non-decreasing
            hull = deque()

            for i in range(1, n + 1):
                # Add line for j = i-1 if it is reachable
                j = i - 1
                if dp_prev[j] < INF:
                    m = -C[j]
                    b = dp_prev[j]
                    # Maintain lower hull: remove last line if it becomes redundant
                    while len(hull) >= 2:
                        m1, b1 = hull[-2]
                        m2, b2 = hull[-1]
                        # Check if middle line (m2, b2) is redundant
                        # Condition: (b2 - b1) * (m2 - m) >= (b - b2) * (m1 - m2)
                        if (b2 - b1) * (m2 - m) >= (b - b2) * (m1 - m2):
                            hull.pop()
                        else:
                            break
                    hull.append((m, b))

                # Query for x = S[i] + k*g
                x = S[i] + k * g
                if not hull:
                    dp_curr[i] = INF
                    continue

                # Pop from front while next line gives smaller value
                while len(hull) >= 2:
                    m1, b1 = hull[0]
                    m2, b2 = hull[1]
                    if m1 * x + b1 >= m2 * x + b2:
                        hull.popleft()
                    else:
                        break
                m_best, b_best = hull[0]
                best = m_best * x + b_best
                # dp_curr[i] = x * C[i] + min_j (dp_prev[j] - x * C[j])
                dp_curr[i] = best + x * C[i]

            dp_prev = dp_curr
            if dp_curr[n] < ans:
                ans = dp_curr[n]

        return ans