import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # cost[i] will store the minimum operations to make nums[i-x+1...i] all equal
        # This corresponds to the window ending at index i (0-indexed)
        # Valid i are from x-1 to n-1
        cost = [0] * n
        
        # We'll use two heaps to maintain the median of the sliding window
        # max_heap for the lower half (stores negative values for Python's min-heap)
        # min_heap for the upper half
        max_heap = []  # lower half
        min_heap = []  # upper half
        
        # Sums of elements in each heap
        sum_lower = 0
        sum_upper = 0
        
        # Helper to balance heaps
        def balance():
            nonlocal sum_lower, sum_upper
            # Ensure len(max_heap) == len(min_heap) or len(max_heap) == len(min_heap) + 1
            while len(max_heap) > len(min_heap) + 1:
                val = -heapq.heappop(max_heap)
                sum_lower -= val
                heapq.heappush(min_heap, val)
                sum_upper += val
            while len(min_heap) > len(max_heap):
                val = heapq.heappop(min_heap)
                sum_upper -= val
                heapq.heappush(max_heap, -val)
                sum_lower += val
        
        # Initialize the first window
        for i in range(x):
            val = nums[i]
            # Add to max_heap initially
            heapq.heappush(max_heap, -val)
            sum_lower += val
            balance()
        
        # Compute cost for first window ending at x-1
        # Median is the top of max_heap
        median = -max_heap[0]
        # Cost = (median * count_lower - sum_lower) + (sum_upper - median * count_upper)
        count_lower = len(max_heap)
        count_upper = len(min_heap)
        cost[x-1] = (median * count_lower - sum_lower) + (sum_upper - median * count_upper)
        
        # Slide the window
        for i in range(x, n):
            # Remove nums[i-x] and add nums[i]
            remove_val = nums[i-x]
            add_val = nums[i]
            
            # Remove remove_val
            # We need to find which heap it's in. We'll use lazy removal or a more robust method.
            # Given constraints and simplicity, we can rebuild if needed, but that's O(x log x).
            # Instead, we'll use a standard approach: mark for removal and clean up lazily.
            # But for simplicity and given x can be large, let's use a different approach:
            # Since k is small, maybe we don't need O(n log x) for cost? 
            # Actually, O(n log x) is acceptable. Let's implement lazy removal.
            pass
        
        # Let's restart the cost calculation with a cleaner approach using sorted list or two heaps with lazy removal.
        # Given the complexity of lazy removal with two heaps, and since x can be up to 10^5, 
        # a simpler O(n * x) is too slow. 
        # Alternative: Use a Fenwick tree or segment tree over the values? Values are in [-1e6, 1e6].
        # We can compress values or use a fixed-size BIT if we offset.
        # But a simpler method: Since we only need the median and sum, we can use the "sliding window median" with two heaps and lazy removal.
        
        # Reset and implement properly with lazy removal
        max_heap = []  # lower half (max heap)
        min_heap = []  # upper half (min heap)
        sum_lower = 0
        sum_upper = 0
        
        # Lazy removal dictionaries
        to_remove_max = {}  # value -> count
        to_remove_min = {}  # value -> count
        
        def push_max(val):
            nonlocal sum_lower
            heapq.heappush(max_heap, -val)
            sum_lower += val
            
        def push_min(val):
            nonlocal sum_upper
            heapq.heappush(min_heap, val)
            sum_upper += val
            
        def remove_max(val):
            nonlocal sum_lower
            to_remove_max[val] = to_remove_max.get(val, 0) + 1
            sum_lower -= val
            
        def remove_min(val):
            nonlocal sum_upper
            to_remove_min[val] = to_remove_min.get(val, 0) + 1
            sum_upper -= val
            
        def get_median():
            # Clean up tops
            while max_heap and to_remove_max.get(-max_heap[0], 0) > 0:
                val = -heapq.heappop(max_heap)
                to_remove_max[val] -= 1
                if to_remove_max[val] == 0:
                    del to_remove_max[val]
            while min_heap and to_remove_min.get(min_heap[0], 0) > 0:
                val = heapq.heappop(min_heap)
                to_remove_min[val] -= 1
                if to_remove_min[val] == 0:
                    del to_remove_min[val]
            return -max_heap[0]
        
        def balance_heaps():
            nonlocal sum_lower, sum_upper
            # Clean up tops first
            while max_heap and to_remove_max.get(-max_heap[0], 0) > 0:
                val = -heapq.heappop(max_heap)
                to_remove_max[val] -= 1
                if to_remove_max[val] == 0:
                    del to_remove_max[val]
            while min_heap and to_remove_min.get(min_heap[0], 0) > 0:
                val = heapq.heappop(min_heap)
                to_remove_min[val] -= 1
                if to_remove_min[val] == 0:
                    del to_remove_min[val]
            
            # Balance sizes
            while len(max_heap) > len(min_heap) + 1:
                val = -heapq.heappop(max_heap)
                sum_lower -= val
                heapq.heappush(min_heap, val)
                sum_upper += val
            while len(min_heap) > len(max_heap):
                val = heapq.heappop(min_heap)
                sum_upper -= val
                heapq.heappush(max_heap, -val)
                sum_lower += val
        
        # Initialize first window
        for i in range(x):
            val = nums[i]
            # Add to max_heap initially
            push_max(val)
            balance_heaps()
        
        # Compute cost for first window
        median = get_median()
        # After getting median, heaps are clean and balanced
        # Recalculate sums? No, sums are maintained.
        count_lower = len(max_heap)
        count_upper = len(min_heap)
        cost[x-1] = (median * count_lower - sum_lower) + (sum_upper - median * count_upper)
        
        # Slide window
        for i in range(x, n):
            remove_val = nums[i-x]
            add_val = nums[i]
            
            # Determine which heap remove_val is in
            # It's in max_heap if remove_val <= median (before removal)
            # But median might change. Safer: check against current median
            median_before = get_median()
            if remove_val <= median_before:
                remove_max(remove_val)
            else:
                remove_min(remove_val)
            
            # Add new value
            # Decide which heap to add to
            median_after_add = get_median() # This might not be accurate if heaps are unbalanced
            # Instead, add to the heap that maintains the order
            if not max_heap or add_val <= -max_heap[0]:
                push_max(add_val)
            else:
                push_min(add_val)
            
            balance_heaps()
            
            # Compute cost
            median = get_median()
            count_lower = len(max_heap)
            count_upper = len(min_heap)
            cost[i] = (median * count_lower - sum_lower) + (sum_upper - median * count_upper)
        
        # DP
        # dp[j][i] = min operations to form j subarrays using first i elements
        # Initialize dp with infinity
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        
        # Base case: 0 subarrays cost 0
        for i in range(n + 1):
            dp[0][i] = 0
        
        for j in range(1, k + 1):
            for i in range(1, n + 1):
                # Option 1: Skip nums[i-1]
                dp[j][i] = dp[j][i-1]
                
                # Option 2: Form a subarray ending at i-1 (covering i-x to i-1)
                if i >= x:
                    # The window is nums[i-x ... i-1], which ends at index i-1 in nums
                    # cost[i-1] is the cost for this window
                    prev = dp[j-1][i-x]
                    if prev != INF:
                        dp[j][i] = min(dp[j][i], prev + cost[i-1])
        
        return dp[k][n]