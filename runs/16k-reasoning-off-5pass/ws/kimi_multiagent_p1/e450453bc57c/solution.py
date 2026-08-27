from typing import List
import heapq
from collections import defaultdict


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1  # number of windows

        # ---- Sliding median absolute deviation via two heaps with lazy deletion ----
        lo = []   # max-heap (store negatives)
        hi = []   # min-heap
        delayed = defaultdict(int)  # value -> pending removal count
        size_lo = 0  # logical sizes (excluding stale entries)
        size_hi = 0
        sum_lo = 0   # logical sums
        sum_hi = 0

        def clean_lo():
            while lo and delayed[-lo[0]] > 0:
                delayed[-lo[0]] -= 1
                heapq.heappop(lo)

        def clean_hi():
            while hi and delayed[hi[0]] > 0:
                delayed[hi[0]] -= 1
                heapq.heappop(hi)

        def rebalance():
            nonlocal size_lo, size_hi, sum_lo, sum_hi
            # invariant: size_lo == size_hi or size_lo == size_hi + 1
            if size_lo > size_hi + 1:
                clean_lo()
                v = -heapq.heappop(lo)
                size_lo -= 1
                sum_lo -= v
                heapq.heappush(hi, v)
                size_hi += 1
                sum_hi += v
            elif size_lo < size_hi:
                clean_hi()
                v = heapq.heappop(hi)
                size_hi -= 1
                sum_hi -= v
                heapq.heappush(lo, -v)
                size_lo += 1
                sum_lo += v

        def add(v):
            nonlocal size_lo, size_hi, sum_lo, sum_hi
            clean_lo()
            if lo and v <= -lo[0]:
                heapq.heappush(lo, -v)
                size_lo += 1
                sum_lo += v
            else:
                heapq.heappush(hi, v)
                size_hi += 1
                sum_hi += v
            rebalance()

        def remove(v):
            nonlocal size_lo, size_hi, sum_lo, sum_hi
            delayed[v] += 1
            clean_lo()
            if lo and v <= -lo[0]:
                size_lo -= 1
                sum_lo -= v
                if lo and -lo[0] == v:
                    clean_lo()
            else:
                size_hi -= 1
                sum_hi -= v
                if hi and hi[0] == v:
                    clean_hi()
            rebalance()

        def window_cost():
            clean_lo()
            med = -lo[0]
            return med * size_lo - sum_lo + sum_hi - med * size_hi

        cost = [0] * m
        for i in range(x):
            add(nums[i])
        cost[0] = window_cost()
        for i in range(1, m):
            remove(nums[i - 1])
            add(nums[i + x - 1])
            cost[i] = window_cost()

        # ---- DP: pick k non-overlapping windows (starts >= x apart) minimizing total cost ----
        INF = float('inf')
        prev = [0] * (m + 1)  # dp for j-1 subarrays
        for j in range(1, k + 1):
            cur = [INF] * (m + 1)
            # cur[i] = min cost using j subarrays among windows with start index < i
            # transition: cur[i] = min(cur[i-1], prev[i-x] + cost[i-1])
            for i in range(1, m + 1):
                best = cur[i - 1]
                if i - x >= 0 and prev[i - x] != INF:
                    cand = prev[i - x] + cost[i - 1]
                    if cand < best:
                        best = cand
                cur[i] = best
            prev = cur
        return prev[m]