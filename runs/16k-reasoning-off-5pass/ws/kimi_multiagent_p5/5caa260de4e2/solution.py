from typing import List
from collections import deque


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums (1-indexed): S[r] = sum(nums[0..r-1]), C[r] = sum(cost[0..r-1])
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = float('inf')
        # prev[l] = dp[i-1][l]: min cost to partition first l elements into i-1 segments
        prev = [INF] * (n + 1)
        prev[0] = 0
        ans = INF

        for i in range(1, n + 1):
            cur = [INF] * (n + 1)
            # Monotone CHT: lines y = m*x + b with m = -C[l], b = prev[l],
            # inserted for l = i-1 .. n-1 (slopes strictly decreasing since C strictly increasing).
            # Queries at x = S[r] + k*i for r = i .. n (x strictly increasing since S strictly increasing).
            hull = deque()  # each entry: (m, b)
            l = i - 1
            for r in range(i, n + 1):
                # Insert line for index l (if reachable) before answering query at r
                if prev[l] < INF:
                    m_new = -C[l]
                    b_new = prev[l]
                    # Maintain lower hull for minimum queries with decreasing slopes.
                    # Evict second-to-last line if it is made useless by the new line.
                    while len(hull) >= 2:
                        m1, b1 = hull[-2]
                        m2, b2 = hull[-1]
                        # line2 is unnecessary if intersection(line1, line2) >= intersection(line1, line_new)
                        # (b2-b1)/(m1-m2) >= (b_new-b1)/(m1-m_new); denominators positive (m1 > m2 > m_new)
                        if (b2 - b1) * (m1 - m_new) >= (b_new - b1) * (m1 - m2):
                            hull.pop()
                        else:
                            break
                    hull.append((m_new, b_new))
                    l += 1
                x = S[r] + k * i
                # Pop front while next line gives a smaller value at x
                while len(hull) >= 2:
                    m1, b1 = hull[0]
                    m2, b2 = hull[1]
                    if m1 * x + b1 >= m2 * x + b2:
                        hull.popleft()
                    else:
                        break
                m, b = hull[0]
                cur[r] = m * x + b + x * C[r]
            ans = min(ans, cur[n])
            prev = cur

        return ans