import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        
        # Precompute costs for all windows of size x
        # cost[i] will store the cost to make nums[i-x+1...i] uniform
        cost = [0] * n
        
        # Two heaps to maintain the median of the current window
        # max_heap stores the lower half (negated values)
        # min_heap stores the upper half
        max_heap = []
        min_heap = []
        
        # Variables to track the sum of elements in both heaps
        sum_lower = 0  # sum of elements in max_heap (actual values)
        sum_upper = 0  # sum of elements in min_heap
        
        # Dictionary for lazy removal
        removed = {}
        
        # Real sizes of the heaps (excluding removed elements)
        real_len_lower = 0
        real_len_upper = 0
        
        # Target sizes
        target_lower = (x + 1) // 2
        target_upper = x // 2
        
        # Initialize first window
        for i in range(x):
            val = nums[i]
            if not max_heap or val <= -max_heap[0]:
                heapq.heappush(max_heap, -val)
                sum_lower += val
                real_len_lower += 1
            else:
                heapq.heappush(min_heap, val)
                sum_upper += val
                real_len_upper += 1
            
            # Balance heaps
            while real_len_lower > target_lower:
                # Clean top of lower first
                while removed.get(-max_heap[0], 0) > 0:
                    val = -heapq.heappop(max_heap)
                    removed[val] -= 1
                    if removed[val] == 0:
                        del removed[val]
                
                val = -heapq.heappop(max_heap)
                sum_lower -= val
                real_len_lower -= 1
                
                heapq.heappush(min_heap, val)
                sum_upper += val
                real_len_upper += 1
                
            while real_len_upper > target_upper:
                # Clean top of upper first
                while removed.get(min_heap[0], 0) > 0:
                    val = heapq.heappop(min_heap)
                    removed[val] -= 1
                    if removed[val] == 0:
                        del removed[val]
                
                val = heapq.heappop(min_heap)
                sum_upper -= val
                real_len_upper -= 1
                
                heapq.heappush(max_heap, -val)
                sum_lower += val
                real_len_lower += 1
        
        # Calculate cost for first window
        while removed.get(-max_heap[0], 0) > 0:
            val = -heapq.heappop(max_heap)
            removed[val] -= 1
            if removed[val] == 0:
                del removed[val]
        
        median = -max_heap[0]
        cost[x-1] = (real_len_lower - real_len_upper) * median + sum_upper - sum_lower
        
        # Slide the window
        for i in range(x, n):
            # Remove element leaving the window: nums[i-x]
            leaving = nums[i-x]
            
            # Clean tops to ensure median is valid before checking where leaving belongs
            while removed.get(-max_heap[0], 0) > 0:
                val = -heapq.heappop(max_heap)
                removed[val] -= 1
                if removed[val] == 0:
                    del removed[val]
            
            current_median = -max_heap[0]
            
            if leaving <= current_median:
                sum_lower -= leaving
                real_len_lower -= 1
                removed[leaving] = removed.get(leaving, 0) + 1
            else:
                sum_upper -= leaving
                real_len_upper -= 1
                removed[leaving] = removed.get(leaving, 0) + 1
            
            # Add nums[i]
            entering = nums[i]
            
            # Re-check median after potential removals? 
            # We need the median of the window [i-x+1 ... i-1] to decide where to put 'entering'.
            # The current tops are valid after the cleaning loop above.
            while removed.get(-max_heap[0], 0) > 0:
                val = -heapq.heappop(max_heap)
                removed[val] -= 1
                if removed[val] == 0:
                    del removed[val]
            
            ref_median = -max_heap[0]
            
            if not max_heap or entering <= ref_median:
                heapq.heappush(max_heap, -entering)
                sum_lower += entering
                real_len_lower += 1
            else:
                heapq.heappush(min_heap, entering)
                sum_upper += entering
                real_len_upper += 1
            
            # Balance heaps
            while real_len_lower > target_lower:
                while removed.get(-max_heap[0], 0) > 0:
                    val = -heapq.heappop(max_heap)
                    removed[val] -= 1
                    if removed[val] == 0:
                        del removed[val]
                
                val = -heapq.heappop(max_heap)
                sum_lower -= val
                real_len_lower -= 1
                
                heapq.heappush(min_heap, val)
                sum_upper += val
                real_len_upper += 1
                
            while real_len_upper > target_upper:
                while removed.get(min_heap[0], 0) > 0:
                    val = heapq.heappop(min_heap)
                    removed[val] -= 1
                    if removed[val] == 0:
                        del removed[val]
                
                val = heapq.heappop(min_heap)
                sum_upper -= val
                real_len_upper -= 1
                
                heapq.heappush(max_heap, -val)
                sum_lower += val
                real_len_lower += 1
            
            # Clean tops to ensure median is valid for cost calculation
            while removed.get(-max_heap[0], 0) > 0:
                val = -heapq.heappop(max_heap)
                removed[val] -= 1
                if removed[val] == 0:
                    del removed[val]
            
            median = -max_heap[0]
            current_cost = (real_len_lower - real_len_upper) * median + sum_upper - sum_lower
            cost[i] = current_cost
            
        # DP to find min operations for k non-overlapping subarrays
        INF = float('inf')
        # dp[j] = min cost to have j subarrays ending at or before the current position
        # We need to store history to access dp[i-x]
        # states[i] will store the dp array after processing index i
        
        # Initialize dp for "before any elements"
        # dp[0] = 0, others = INF
        current_dp = [0] + [INF] * k
        states = []
        
        # Pre-fill states for i < x-1 (no subarray can end)
        for _ in range(x - 1):
            states.append(current_dp[:])
        
        # Loop for i >= x-1
        for i in range(x - 1, n):
            next_dp = current_dp[:]
            prev_state = states[i - x]
            c = cost[i]
            for j in range(1, k + 1):
                if prev_state[j - 1] != INF:
                    val = prev_state[j - 1] + c
                    if val < next_dp[j]:
                        next_dp[j] = val
            states.append(next_dp)
            current_dp = next_dp
            
        return current_dp[k]