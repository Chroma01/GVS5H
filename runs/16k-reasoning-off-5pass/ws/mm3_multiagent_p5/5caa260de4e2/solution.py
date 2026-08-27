import sys
sys.setrecursionlimit(1000000)
from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Compute prefix sums
        A = [0] * (n + 1)
        B = [0] * (n + 1)
        for i in range(n):
            A[i+1] = A[i] + nums[i]
            B[i+1] = B[i] + cost[i]
        
        INF = float('inf')
        dp_prev = [INF] * (n + 1)
        dp_prev[0] = 0
        
        def compute(g, dp_prev, dp_curr, l, r, optL, optR):
            if l > r:
                return
            mid = (l + r) // 2
            best = INF
            best_k = -1
            start = optL
            end = min(mid - 1, optR)
            if start <= end:
                for j in range(start, end + 1):
                    if dp_prev[j] == INF:
                        continue
                    val = dp_prev[j] + (A[mid] - A[j] + k * g) * (B[mid] - B[j])
                    if val < best:
                        best = val
                        best_k = j
            dp_curr[mid] = best
            if best_k != -1:
                compute(g, dp_prev, dp_curr, l, mid - 1, optL, best_k)
                compute(g, dp_prev, dp_curr, mid + 1, r, best_k, optR)
            else:
                compute(g, dp_prev, dp_curr, l, mid - 1, optL, optR)
                compute(g, dp_prev, dp_curr, mid + 1, r, optL, optR)
        
        for g in range(1, n + 1):
            dp_curr = [INF] * (n + 1)
            compute(g, dp_prev, dp_curr, g, n, g - 1, n - 1)
            dp_prev = dp_curr
        
        return min(dp_prev)