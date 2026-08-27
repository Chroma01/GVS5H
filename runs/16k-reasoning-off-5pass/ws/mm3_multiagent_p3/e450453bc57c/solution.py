from typing import List
import heapq

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        if x > n:
            return 0  # Should not happen per constraints
        
        # Compute cost[i] = min ops to make window nums[i-x+1..i] constant
        cost = [0] * n
        
        # Two-heap structure with lazy deletion
        max_heap = []  # max-heap (stores negatives)
        min_heap = []  # min-heap
        sum_lower = 0  # sum of elements in max_heap
        sum_upper = 0  # sum of elements in min_heap
        delayed = {}   # value -> count for lazy deletion
        target_lower = (x + 1) // 2  # size of max_heap
        
        def clean(heap):
            while heap:
                val = -heap[0] if heap is max_heap else heap[0]
                cnt = delayed.get(val, 0)
                if cnt:
                    heapq.heappop(heap)
                    if cnt == 1:
                        del delayed[val]
                    else:
                        delayed[val] = cnt - 1
                else:
                    break
        
        def balance():
            # Ensure size
            if len(max_heap) > target_lower:
                val = -heapq.heappop(max_heap)
                sum_lower -= val
                heapq.heappush(min_heap, val)
                sum_upper += val
            elif len(max_heap) < target_lower and min_heap:
                val = heapq.heappop(min_heap)
                sum_upper -= val
                heapq.heappush(max_heap, -val)
                sum_lower += val
            # Ensure ordering
            clean(max_heap)
            clean(min_heap)
            if max_heap and min_heap and -max_heap[0] > min_heap[0]:
                a = -heapq.heappop(max_heap)
                b = heapq.heappop(min_heap)
                sum_lower -= a
                sum_lower += b
                sum_upper -= b
                sum_upper += a
                heapq.heappush(max_heap, -b)
                heapq.heappush(min_heap, a)
        
        def add_num(num):
            nonlocal sum_lower, sum_upper
            clean(max_heap)
            clean(min_heap)
            if not max_heap or num <= -max_heap[0]:
                heapq.heappush(max_heap, -num)
                sum_lower += num
            else:
                heapq.heappush(min_heap, num)
                sum_upper += num
            balance()
        
        def remove_num(num):
            nonlocal sum_lower, sum_upper
            clean(max_heap)
            clean(min_heap)
            median = -max_heap[0] if max_heap else 0
            if num <= median:
                sum_lower -= num
            else:
                sum_upper -= num
            delayed[num] = delayed.get(num, 0) + 1
        
        # Initialize first window [0..x-1]
        for i in range(x):
            add_num(nums[i])
        # Record cost for window ending at index x-1
        clean(max_heap)
        clean(min_heap)
        median = -max_heap[0]
        cost[x-1] = median * len(max_heap) - sum_lower + sum_upper - median * len(min_heap)
        
        # Slide window
        for i in range(x, n):
            remove_num(nums[i - x])
            add_num(nums[i])
            clean(max_heap)
            clean(min_heap)
            median = -max_heap[0]
            cost[i] = median * len(max_heap) - sum_lower + sum_upper - median * len(min_heap)
        
        # DP: prev[i] = min cost for t-1 windows in first i elements
        INF = 10**18
        prev = [0] * (n + 1)  # t=0: cost 0 for any prefix
        
        for t in range(1, k + 1):
            curr = [INF] * (n + 1)
            for i in range(1, n + 1):
                # Option 1: skip nums[i-1]
                best = curr[i-1]
                # Option 2: end a window at i (window covers i-x .. i-1)
                if i >= x:
                    candidate = prev[i - x] + cost[i - 1]
                    if candidate < best:
                        best = candidate
                curr[i] = best
            prev = curr
        
        return prev[n]