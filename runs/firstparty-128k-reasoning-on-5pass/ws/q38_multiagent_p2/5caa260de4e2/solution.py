from typing import List
from collections import deque

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums of nums and cost.
        pnum = [0] * (n + 1)
        pcost = [0] * (n + 1)
        for i in range(n):
            pnum[i + 1] = pnum[i] + nums[i]
            pcost[i + 1] = pcost[i] + cost[i]

        INF = 10 ** 30

        # dp_prev[j] = minimum cost to partition first j elements
        # into exactly t-1 subarrays.
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0

        ans = INF

        # t = number of subarrays in the current layer.
        for t in range(1, n + 1):
            dp_cur = [INF] * (n + 1)
            hull = deque()
            kt = k * t

            # i = number of elements in the prefix being partitioned.
            for i in range(t, n + 1):
                # Add the line corresponding to previous cut j = i - 1.
                j = i - 1
                prev = dp_prev[j]
                if prev < INF:
                    m = -pcost[j]
                    b = prev

                    # Maintain lower hull for decreasing slopes.
                    # For lines l1, l2, l3 with m1 > m2 > m3,
                    # l2 is useless if intersection(l1,l2) >= intersection(l2,l3).
                    while len(hull) >= 2:
                        m1, b1 = hull[-2]
                        m2, b2 = hull[-1]
                        if (b2 - b1) * (m2 - m) >= (b - b2) * (m1 - m2):
                            hull.pop()
                        else:
                            break

                    hull.append((m, b))

                # Query the hull at x = pnum[i] + k*t.
                if hull:
                    x = pnum[i] + kt

                    # Query x is increasing, so pop obsolete front lines.
                    while len(hull) >= 2:
                        m1, b1 = hull[0]
                        m2, b2 = hull[1]
                        if m1 * x + b1 >= m2 * x + b2:
                            hull.popleft()
                        else:
                            break

                    m, b = hull[0]
                    dp_cur[i] = x * pcost[i] + m * x + b

            if dp_cur[n] < ans:
                ans = dp_cur[n]

            dp_prev = dp_cur

        return ans