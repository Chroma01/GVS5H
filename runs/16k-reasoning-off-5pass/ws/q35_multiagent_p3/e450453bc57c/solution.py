import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        
        # Precompute costs for all windows of size x
        # cost[i] is the cost to make nums[i:i+x] all equal to the median
        cost = [0] * (n - x + 1)
        
        # Sliding window median using two heaps with lazy removal
        left = []  # max-heap (store negative values)
        right = [] # min-heap
        left_sum = 0
        right_sum = 0
        left_count = 0
        right_count = 0
        
        # Lazy removal dictionaries
        left_removed = {}
        right_removed = {}
        
        def add_to_left(val):
            nonlocal left_sum, left_count
            heapq.heappush(left, -val)
            left_sum += val
            left_count += 1
            
        def add_to_right(val):
            nonlocal right_sum, right_count
            heapq.heappush(right, val)
            right_sum += val
            right_count += 1
            
        def remove_from_left(val):
            nonlocal left_sum, left_count
            left_removed[val] = left_removed.get(val, 0) + 1
            left_sum -= val
            left_count -= 1
            
        def remove_from_right(val):
            nonlocal right_sum, right_count
            right_removed[val] = right_removed.get(val, 0) + 1
            right_sum -= val
            right_count -= 1
            
        def get_median():
            # Clean up tops
            while left and left_removed.get(-left[0], 0) > 0:
                val = -heapq.heappop(left)
                left_removed[val] -= 1
                if left_removed[val] == 0:
                    del left_removed[val]
            while right and right_removed.get(right[0], 0) > 0:
                val = heapq.heappop(right)
                right_removed[val] -= 1
                if right_removed[val] == 0:
                    del right_removed[val]
            
            # Rebalance: left should have ceil(x/2) elements, right should have floor(x/2)
            # Actually, for even x, we can have left have x//2 and right have x//2, 
            # and median is left[0] (lower median).
            # For odd x, left has (x+1)//2, right has (x-1)//2.
            # We maintain: len(left) == (total + 1) // 2
            total = left_count + right_count
            while left_count > (total + 1) // 2:
                # Move from left to right
                while left and left_removed.get(-left[0], 0) > 0:
                    val = -heapq.heappop(left)
                    left_removed[val] -= 1
                    if left_removed[val] == 0:
                        del left_removed[val]
                val = -heapq.heappop(left)
                left_sum -= val
                left_count -= 1
                right_sum += val
                right_count += 1
                heapq.heappush(right, val)
            while left_count < (total + 1) // 2:
                # Move from right to left
                while right and right_removed.get(right[0], 0) > 0:
                    val = heapq.heappop(right)
                    right_removed[val] -= 1
                    if right_removed[val] == 0:
                        del right_removed[val]
                val = heapq.heappop(right)
                right_sum -= val
                right_count -= 1
                left_sum += val
                left_count += 1
                heapq.heappush(left, -val)
            
            # Clean up tops again after rebalancing
            while left and left_removed.get(-left[0], 0) > 0:
                val = -heapq.heappop(left)
                left_removed[val] -= 1
                if left_removed[val] == 0:
                    del left_removed[val]
            while right and right_removed.get(right[0], 0) > 0:
                val = heapq.heappop(right)
                right_removed[val] -= 1
                if right_removed[val] == 0:
                    del right_removed[val]
            
            return -left[0]
        
        # Initialize first window
        for i in range(x):
            if i < x // 2:
                add_to_left(nums[i])
            else:
                add_to_right(nums[i])
        
        # Compute cost for first window
        median = get_median()
        cost[0] = (right_sum - median * right_count) + (median * left_count - left_sum)
        
        # Slide window
        for i in range(1, n - x + 1):
            # Remove nums[i-1]
            val_out = nums[i-1]
            # Determine which heap it was in
            # It was in left if val_out <= median_prev, but we don't track that easily.
            # Instead, we can check: if val_out <= -left[0] (after cleaning), it was in left? 
            # But heaps might have stale values. 
            # Better: when adding, we know. But for removal, we need to know.
            # Alternative: use a different approach for removal: 
            # Actually, the standard lazy removal doesn't require knowing which heap to remove from if we just mark it.
            # But we need to know which heap to decrement sum/count from.
            # We can determine by comparing with current median? Not reliable due to stale values.
            
            # Correct approach: when we add, we push to one heap. When we remove, we must know which heap.
            # We can store the heap assignment? Or, we can use the fact that if val_out <= median of previous window, it was in left?
            # But median changes. 
            # Actually, a simpler method: maintain the invariant that all elements in left <= all in right.
            # When removing, if val_out <= -left[0] (cleaned), it's in left, else in right.
            # But we need to clean tops first.
            
            # Clean tops
            while left and left_removed.get(-left[0], 0) > 0:
                val = -heapq.heappop(left)
                left_removed[val] -= 1
                if left_removed[val] == 0:
                    del left_removed[val]
            while right and right_removed.get(right[0], 0) > 0:
                val = heapq.heappop(right)
                right_removed[val] -= 1
                if right_removed[val] == 0:
                    del right_removed[val]
            
            # Now, determine which heap val_out is in
            if left and val_out <= -left[0]:
                remove_from_left(val_out)
            else:
                remove_from_right(val_out)
            
            # Add nums[i+x-1]
            val_in = nums[i+x-1]
            # Add to appropriate heap to maintain order
            if left and val_in < -left[0]:
                add_to_left(val_in)
            else:
                add_to_right(val_in)
            
            # Rebalance
            total = left_count + right_count
            while left_count > (total + 1) // 2:
                while left and left_removed.get(-left[0], 0) > 0:
                    val = -heapq.heappop(left)
                    left_removed[val] -= 1
                    if left_removed[val] == 0:
                        del left_removed[val]
                val = -heapq.heappop(left)
                left_sum -= val
                left_count -= 1
                right_sum += val
                right_count += 1
                heapq.heappush(right, val)
            while left_count < (total + 1) // 2:
                while right and right_removed.get(right[0], 0) > 0:
                    val = heapq.heappop(right)
                    right_removed[val] -= 1
                    if right_removed[val] == 0:
                        del right_removed[val]
                val = heapq.heappop(right)
                right_sum -= val
                right_count -= 1
                left_sum += val
                left_count += 1
                heapq.heappush(left, -val)
            
            # Clean tops
            while left and left_removed.get(-left[0], 0) > 0:
                val = -heapq.heappop(left)
                left_removed[val] -= 1
                if left_removed[val] == 0:
                    del left_removed[val]
            while right and right_removed.get(right[0], 0) > 0:
                val = heapq.heappop(right)
                right_removed[val] -= 1
                if right_removed[val] == 0:
                    del right_removed[val]
            
            median = -left[0]
            cost[i] = (right_sum - median * right_count) + (median * left_count - left_sum)
            
        # DP to find minimum operations for k non-overlapping subarrays
        # dp[j] = min cost to form j subarrays
        # We use a 1D DP array, but we need to be careful about order.
        # dp[j][i] = min cost to form j subarrays using first i elements.
        # dp[j][i] = min(dp[j][i-1], dp[j-1][i-x] + cost[i-x]) if i >= x
        # We can optimize space to O(k) by iterating backwards for j.
        
        INF = float('inf')
        dp = [INF] * (k + 1)
        dp[0] = 0
        
        # We iterate through each possible end position of the last subarray
        # The last subarray ends at index i (0-indexed), so it starts at i-x+1.
        # In terms of our cost array, cost[i-x+1] corresponds to the subarray starting at i-x+1.
        # Let's define: for each start index s from 0 to n-x, the subarray is nums[s:s+x].
        # dp[j] after processing up to some point represents the min cost to form j subarrays 
        # using a subset of subarrays that end at or before the current position.
        
        # Actually, let's use the standard interval DP:
        # Let dp[j] be the min cost to form j subarrays, where the last subarray ends at the current position being considered.
        # But we need to ensure non-overlapping. 
        # Better: dp[j] = min cost to form j subarrays using elements from nums[0...i-1].
        # We iterate i from 0 to n.
        # For each i, if i >= x, we can form a subarray ending at i-1 (starting at i-x).
        # Then dp[j] = min(dp[j], dp_prev[j-1] + cost[i-x]) where dp_prev is the dp state before considering the subarray ending at i-1.
        
        # We'll use a 2D array for clarity, then optimize if needed. Given k<=15, O(k*N) is fine.
        dp2 = [[INF] * (n + 1) for _ in range(k + 1)]
        for i in range(n + 1):
            dp2[0][i] = 0
            
        for j in range(1, k + 1):
            for i in range(1, n + 1):
                # Option 1: don't end a subarray at i-1
                dp2[j][i] = dp2[j][i-1]
                # Option 2: end a subarray at i-1 (so subarray is nums[i-x:i])
                if i >= x:
                    prev = dp2[j-1][i-x]
                    if prev != INF:
                        dp2[j][i] = min(dp2[j][i], prev + cost[i-x])
                        
        return dp2[k][n]