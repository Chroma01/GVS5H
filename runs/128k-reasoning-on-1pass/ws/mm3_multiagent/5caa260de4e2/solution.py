from typing import List
from collections import deque

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # prefix sums
        pref_n = [0] * n
        pref_c = [0] * n
        for i in range(n):
            pref_n[i] = (pref_n[i - 1] if i else 0) + nums[i]
            pref_c[i] = (pref_c[i - 1] if i else 0) + cost[i]

        INF = 10 ** 30
        dp_prev = [INF] * n  # dp for (c-1) subarrays, initially unused
        answer = INF

        # helper functions for convex hull trick
        def value(line, x):
            m, b = line
            return m * x + b

        def bad(l1, l2, l3):
            # return True if l2 is unnecessary (minimum hull)
            m1, b1 = l1
            m2, b2 = l2
            m3, b3 = l3
            # (b2 - b1)*(m2 - m3) >= (b3 - b2)*(m1 - m2)
            return (b2 - b1) * (m2 - m3) >= (b3 - b2) * (m1 - m2)

        for c in range(1, n + 1):
            dp_curr = [INF] * n
            hull = deque()
            if c == 1:
                # line for empty prefix: slope 0, intercept 0
                hull.append((0, 0))
            # else: hull starts empty

            for i in range(n):
                # add line for j = i-1 if it corresponds to a valid prefix
                if c > 1 and i > 0 and dp_prev[i - 1] != INF:
                    m = -pref_c[i - 1]
                    b = dp_prev[i - 1]
                    # maintain lower convex hull
                    while len(hull) >= 2 and bad(hull[-2], hull[-1], (m, b)):
                        hull.pop()
                    hull.append((m, b))

                # query hull if we can form c subarrays up to i
                if i >= c - 1 and hull:
                    x = pref_n[i] + k * c
                    # discard lines that are worse for current x
                    while len(hull) >= 2 and value(hull[0], x) >= value(hull[1], x):
                        hull.popleft()
                    best = value(hull[0], x)
                    dp_curr[i] = (pref_n[i] + k * c) * pref_c[i] + best

            answer = min(answer, dp_curr[n - 1])
            dp_prev = dp_curr

        return answer