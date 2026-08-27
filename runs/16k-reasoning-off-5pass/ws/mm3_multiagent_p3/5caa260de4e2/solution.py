from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        P = [0] * (n + 1)   # prefix sum of nums
        C = [0] * (n + 1)   # prefix sum of cost
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        INF = 10 ** 30

        # dp_prev[i] = dp[g-1][i], dp_cur[i] = dp[g][i]
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0  # zero elements with zero subarrays costs nothing

        def compute(l: int, r: int, optL: int, optR: int,
                    g: int, dp_prev: List[int], dp_cur: List[int],
                    P: List[int], C: List[int], k: int) -> None:
            if l > r:
                return
            mid = (l + r) // 2
            best_val = INF
            best_k = -1
            # valid j is in [optL, min(optR, mid-1)]
            start = optL
            end = min(optR, mid - 1)
            for j in range(start, end + 1):
                val = (dp_prev[j]
                       + (P[mid] - P[j] + k * g) * (C[mid] - C[j]))
                if val < best_val:
                    best_val = val
                    best_k = j
            dp_cur[mid] = best_val
            # Recurse on left and right halves, restricting opt ranges
            compute(l, mid - 1, optL, best_k, g, dp_prev, dp_cur, P, C, k)
            compute(mid + 1, r, best_k, optR, g, dp_prev, dp_cur, P, C, k)

        answer = INF
        for g in range(1, n + 1):
            dp_cur = [INF] * (n + 1)
            # for g subarrays, j can range over [0, n-1]; i ranges over [1, n]
            compute(1, n, 0, n - 1, g, dp_prev, dp_cur, P, C, k)
            if dp_cur[n] < answer:
                answer = dp_cur[n]
            dp_prev = dp_cur

        return answer