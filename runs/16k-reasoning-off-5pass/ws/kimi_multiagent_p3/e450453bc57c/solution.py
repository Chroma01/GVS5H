import heapq
from collections import Counter
from typing import List


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        m = n - x + 1  # number of windows

        # ---- Sliding median with two heaps + lazy deletion ----
        # lo: max-heap (store negated), hi: min-heap
        # invariant: len(lo) == len(hi) or len(lo) == len(hi) + 1
        lo = []
        hi = []
        sum_lo = 0
        sum_hi = 0
        delayed = Counter()   # value -> count pending removal
        lo_size = 0           # logical sizes (excluding delayed elements)
        hi_size = 0

        def prune(heap, is_lo):
            # remove logically-deleted elements from the top of the heap
            while heap:
                v = -heap[0] if is_lo else heap[0]
                if delayed.get(v, 0) > 0:
                    delayed[v] -= 1
                    if delayed[v] == 0:
                        del delayed[v]
                    heapq.heappop(heap)
                else:
                    break

        def rebalance():
            nonlocal sum_lo, sum_hi, lo_size, hi_size
            # ensure lo has same size as hi or one more
            if lo_size > hi_size + 1:
                prune(lo, True)
                v = -heapq.heappop(lo)
                lo_size -= 1
                sum_lo -= v
                heapq.heappush(hi, v)
                hi_size += 1
                sum_hi += v
                prune(lo, True)
            elif lo_size < hi_size:
                prune(hi, False)
                v = heapq.heappop(hi)
                hi_size -= 1
                sum_hi -= v
                heapq.heappush(lo, -v)
                lo_size += 1
                sum_lo += v
                prune(hi, False)

        def add(v):
            nonlocal sum_lo, sum_hi, lo_size, hi_size
            prune(lo, True)
            med = -lo[0] if lo else None
            if med is None or v <= med:
                heapq.heappush(lo, -v)
                lo_size += 1
                sum_lo += v
            else:
                heapq.heappush(hi, v)
                hi_size += 1
                sum_hi += v
            rebalance()

        def remove(v):
            nonlocal sum_lo, sum_hi, lo_size, hi_size
            delayed[v] += 1
            prune(lo, True)
            med = -lo[0] if lo else None
            if med is not None and v <= med:
                lo_size -= 1
                sum_lo -= v
                if lo and -lo[0] == v:
                    prune(lo, True)
            else:
                hi_size -= 1
                sum_hi -= v
                if hi and hi[0] == v:
                    prune(hi, False)
            rebalance()

        cost = [0] * m
        for i in range(n):
            add(nums[i])
            if i >= x:
                remove(nums[i - x])
            if i >= x - 1:
                prune(lo, True)
                med = -lo[0]
                # cost to make all elements equal to median
                c = med * lo_size - sum_lo + sum_hi - med * hi_size
                cost[i - x + 1] = c

        # ---- DP: choose exactly k non-overlapping windows with min total cost ----
        # dp[i][j] = min(dp[i+1][j], cost[i] + dp[i+x][j-1])
        INF = float('inf')
        base = [INF] * (k + 1)
        base[0] = 0
        # ring buffer of rows; all indices >= m share the base row
        ring = [base] * (x + 1)

        ans_row = None
        for i in range(m - 1, -1, -1):
            row_i_plus_1 = ring[(i + 1) % (x + 1)]
            row_i_plus_x = ring[(i + x) % (x + 1)]
            cur = [INF] * (k + 1)
            cur[0] = 0
            ci = cost[i]
            for j in range(1, k + 1):
                skip = row_i_plus_1[j]
                take = ci + row_i_plus_x[j - 1]
                cur[j] = skip if skip < take else take
            ring[i % (x + 1)] = cur
            if i == 0:
                ans_row = cur

        return ans_row[k]