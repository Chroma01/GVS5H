import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        
        # Precompute costs for all subarrays of size x
        # cost[i] is the cost to make nums[i-x+1 ... i] all equal
        cost = [0] * n
        
        # Two heaps for median maintenance
        # left: max-heap (store negative values)
        # right: min-heap
        left = []  # max-heap
        right = [] # min-heap
        sum_left = 0
        sum_right = 0
        
        # Lazy removal dictionaries
        lazy_left = {}  # value -> count to remove from left
        lazy_right = {} # value -> count to remove from right
        
        def get_median():
            # Clean tops
            while left and lazy_left.get(-left[0], 0) > 0:
                val = -heapq.heappop(left)
                lazy_left[val] -= 1
                if lazy_left[val] == 0:
                    del lazy_left[val]
            while right and lazy_right.get(right[0], 0) > 0:
                val = heapq.heappop(right)
                lazy_right[val] -= 1
                if lazy_right[val] == 0:
                    del lazy_right[val]
            
            # Rebalance so that len(left) == len(right) or len(left) == len(right) + 1
            # We maintain: len(left) >= len(right) and len(left) - len(right) <= 1
            while len(left) > len(right) + 1:
                val = -heapq.heappop(left)
                heapq.heappush(right, val)
                sum_left -= val
                sum_right += val
            while len(left) < len(right):
                val = heapq.heappop(right)
                heapq.heappush(left, -val)
                sum_right -= val
                sum_left += val
            
            # Clean tops again after rebalancing
            while left and lazy_left.get(-left[0], 0) > 0:
                val = -heapq.heappop(left)
                lazy_left[val] -= 1
                if lazy_left[val] == 0:
                    del lazy_left[val]
            while right and lazy_right.get(right[0], 0) > 0:
                val = heapq.heappop(right)
                lazy_right[val] -= 1
                if lazy_right[val] == 0:
                    del lazy_right[val]
            
            return -left[0]
        
        def add_to_window(val):
            nonlocal sum_left, sum_right
            # Add val to left or right
            if not left or val <= -left[0]:
                heapq.heappush(left, -val)
                sum_left += val
            else:
                heapq.heappush(right, val)
                sum_right += val
            
            # Rebalance
            while len(left) > len(right) + 1:
                val = -heapq.heappop(left)
                heapq.heappush(right, val)
                sum_left -= val
                sum_right += val
            while len(left) < len(right):
                val = heapq.heappop(right)
                heapq.heappush(left, -val)
                sum_right -= val
                sum_left += val
        
        def remove_from_window(val):
            nonlocal sum_left, sum_right
            # Mark for lazy removal
            # Determine which heap it belongs to
            # We need to know if val is in left or right.
            # Since we might have duplicates, we check against current median.
            # But actually, we can just try to remove from both? No, that's inefficient.
            # Better: when adding, we know where it went. But for sliding window, 
            # we need to know where the outgoing element is.
            # Alternative: use a balanced BST approach? Not available in Python.
            # Instead, we can use a different strategy: 
            # We'll maintain the heaps such that we can identify membership.
            # Actually, a simpler lazy removal: 
            # We'll store the actual values in the heaps. When removing, we mark it.
            # But we need to know which heap to mark. 
            # Heuristic: if val <= median, it's in left, else in right.
            # But median changes. 
            # Correct approach: 
            # We can use two heaps but also keep a dictionary of counts for each value in the window.
            # Then when removing, we decrement count. When cleaning, we remove from heap if count is 0.
            # But this doesn't help with finding which heap the element is in.
            
            # Let's use a different method: 
            # We will not use lazy removal for the outgoing element directly.
            # Instead, we will rebuild the heaps when the window slides? 
            # That would be O(x) per slide, total O(n*x) which is too slow.
            
            # Correct lazy removal with two heaps:
            # We need to know if the element to remove is in left or right.
            # We can maintain a separate counter for each value in the window.
            # And we can also maintain the current median.
            # When removing val, if val <= median, it should be in left, else in right.
            # But due to duplicates and rebalancing, this might not be exact.
            
            # Actually, a robust way:
            # Use a balanced BST simulation? Not in Python.
            # Use two heaps with lazy removal, and when removing, we just mark it.
            # But we must know which heap to mark.
            # We can check: if val <= -left[0] (current median), then it's in left.
            # But after rebalancing, the median might change.
            # However, at the time of removal, we can determine based on current state.
            
            # Let's get current median first (cleaning tops)
            while left and lazy_left.get(-left[0], 0) > 0:
                v = -heapq.heappop(left)
                lazy_left[v] -= 1
                if lazy_left[v] == 0:
                    del lazy_left[v]
            while right and lazy_right.get(right[0], 0) > 0:
                v = heapq.heappop(right)
                lazy_right[v] -= 1
                if lazy_right[v] == 0:
                    del lazy_right[v]
            
            median = -left[0] if left else 0
            
            if val <= median:
                lazy_left[val] = lazy_left.get(val, 0) + 1
                sum_left -= val
            else:
                lazy_right[val] = lazy_right.get(val, 0) + 1
                sum_right -= val
        
        # Initialize the first window
        for i in range(x):
            add_to_window(nums[i])
        
        # Calculate cost for first window
        median = get_median()
        cost[x-1] = (median * len(left) - sum_left) + (sum_right - median * len(right))
        
        # Slide the window
        for i in range(x, n):
            # Remove nums[i-x]
            remove_from_window(nums[i-x])
            # Add nums[i]
            add_to_window(nums[i])
            
            # Clean and get median
            median = get_median()
            # Recalculate sizes after cleaning and rebalancing
            # Note: get_median already rebalances
            cost[i] = (median * len(left) - sum_left) + (sum_right - median * len(right))
        
        # DP: dp[j] = min operations to form j non-overlapping subarrays
        # We use a 1D DP array, but we need to be careful about overwriting.
        # dp[i][j] = min cost to form j subarrays using first i elements
        # Transition: 
        #   dp[i][j] = dp[i-1][j]  (skip element i-1)
        #   if i >= x: dp[i][j] = min(dp[i][j], dp[i-x][j-1] + cost[i-1])
        # We can use a 2D array of size (n+1) x (k+1)
        
        INF = float('inf')
        dp = [[INF] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0
        
        for i in range(1, n + 1):
            for j in range(k + 1):
                # Option 1: skip element i-1
                dp[i][j] = dp[i-1][j]
                # Option 2: form a subarray ending at i-1 (if possible)
                if i >= x and j >= 1:
                    prev = dp[i-x][j-1]
                    if prev != INF:
                        dp[i][j] = min(dp[i][j], prev + cost[i-1])
        
        return dp[n][k]