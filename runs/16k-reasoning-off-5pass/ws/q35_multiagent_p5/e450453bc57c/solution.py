import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        
        # Precompute costs for all windows of size x
        # cost[i] is the min operations to make nums[i-x+1...i] all equal
        # We use two heaps to maintain the median and sum of absolute differences
        # left: max-heap (store negative values) for lower half
        # right: min-heap for upper half
        # We maintain: len(left) == len(right) or len(left) == len(right) + 1
        
        left = []  # max-heap
        right = [] # min-heap
        sum_left = 0
        sum_right = 0
        
        # Initialize first window
        for i in range(x):
            val = nums[i]
            # Add to left initially
            heapq.heappush(left, -val)
            sum_left += val
            
            # Balance: ensure len(left) >= len(right) and len(left) - len(right) <= 1
            if len(right) > 0 and -left[0] > right[0]:
                # Move largest from left to right
                l_val = -heapq.heappop(left)
                sum_left -= l_val
                heapq.heappush(right, l_val)
                sum_right += l_val
            
            # If left has more than one extra, move smallest from right to left? 
            # Actually, we want len(left) == ceil(x/2)
            # After adding one element, if len(left) > len(right) + 1, move from left to right
            if len(left) > len(right) + 1:
                r_val = -heapq.heappop(left)
                sum_left -= r_val
                heapq.heappush(right, r_val)
                sum_right += r_val
        
        # Calculate cost for first window
        median = -left[0]
        cost_first = sum_left + sum_right - median * (2 * len(left) - x)
        # Explanation: 
        # sum(|v - median|) for v in left: median * len(left) - sum_left
        # sum(|v - median|) for v in right: sum_right - median * len(right)
        # Total = median * len(left) - sum_left + sum_right - median * len(right)
        #       = sum_right - sum_left + median * (len(left) - len(right))
        # Since len(left) - len(right) is 0 or 1:
        # If x is odd, len(left) = len(right)+1, so diff=1
        # If x is even, len(left) = len(right), so diff=0
        # But note: for even x, any value between the two medians minimizes the sum.
        # Using the lower median (from left) is fine.
        # Actually, the formula: 
        #   cost = (sum_right - sum_left) + median * (len(left) - len.right)
        # Let's verify with an example: [1,2,3], median=2, left=[1,2] (as max-heap: [-2,-1]), right=[3]
        # sum_left=3, sum_right=3, len(left)=2, len(right)=1
        # cost = (3-3) + 2*(1) = 2. Correct: |1-2|+|2-2|+|3-2|=1+0+1=2.
        # Example: [1,2,3,4], median=2 (lower), left=[1,2], right=[3,4]
        # sum_left=3, sum_right=7, len(left)=2, len(right)=2
        # cost = (7-3) + 2*(0) = 4. Correct: |1-2|+|2-2|+|3-2|+|4-2|=1+0+1+2=4.
        
        costs = [0] * n
        costs[x-1] = (sum_right - sum_left) + median * (len(left) - len(right))
        
        # Slide the window
        for i in range(x, n):
            # Remove nums[i-x] and add nums[i]
            out_val = nums[i-x]
            in_val = nums[i]
            
            # Remove out_val
            # We need to find out_val in left or right and remove it.
            # Since we don't have a direct remove from heap, we'll use lazy removal or rebuild?
            # Actually, for a sliding window median with two heaps, lazy removal is tricky because we need to balance.
            # Alternative: since x can be large, but n is 10^5, and we do n steps, O(n log x) is acceptable.
            # But removing an arbitrary element from a heap is O(n). 
            # Instead, we can use a different approach: maintain the heaps and use lazy deletion with a hash map of counts to delete.
            # However, a simpler method for competitive programming when x is not too large is to just rebuild the heaps for each window? That would be O(n * x log x) which is too slow.
            
            # Better approach: Use a balanced BST or sorted list? In Python, we can use the `sortedcontainers` library but it's not available.
            # Alternative: Use two heaps with lazy deletion.
            
            # Let's implement lazy deletion.
            # We'll maintain heaps and a dictionary of elements to be removed.
            # But balancing becomes complex.
            
            # Actually, a standard technique for sliding window median is to use two heaps with lazy removal.
            # We'll maintain:
            #   left: max-heap for lower half
            #   right: min-heap for upper half
            #   lazy_left: count of elements in left that are marked for deletion
            #   lazy_right: count of elements in right that are marked for deletion
            #   sum_left, sum_right: current sums of active elements in each heap
            
            # For simplicity and given constraints (n=10^5, x up to 10^5, k<=15), 
            # and since the window slides one by one, we can do the following:
            # Instead of lazy removal, we can rebuild the heaps for each window? 
            # Rebuilding takes O(x log x) per window, total O(n x log x) which is 10^10 in worst case -> TLE.
            
            # We must use lazy removal.
            
            # Let's restart the heap maintenance with lazy removal.
            pass
        
        # Due to complexity of lazy removal with two heaps and balancing, 
        # and given that k is small, we can use a different DP state representation.
        # Actually, we can precompute costs using a simpler method if we note that x is fixed.
        # But x can be up to 10^5.
        
        # Let's implement the lazy removal approach properly.
        
        # Reset heaps
        left = []
        right = []
        sum_left = 0
        sum_right = 0
        lazy_left = {}
        lazy_right = {}
        
        def balance_heaps():
            nonlocal sum_left, sum_right
            # Clean up lazy deletions from top of left
            while left and -left[0] in lazy_left and lazy_left[-left[0]] > 0:
                val = -heapq.heappop(left)
                lazy_left[val] -= 1
                if lazy_left[val] == 0:
                    del lazy_left[val]
                # Note: we don't adjust sum here because sum is maintained during add/remove
            while right and right[0] in lazy_right and lazy_right[right[0]] > 0:
                val = heapq.heappop(right)
                lazy_right[val] -= 1
                if lazy_right[val] == 0:
                    del lazy_right[val]
            
            # Balance sizes: we want len(active left) == ceil(x/2) and len(active right) == floor(x/2)
            # But we don't track active sizes directly. Instead, we balance by moving elements.
            # Let's define: we want the number of active elements in left to be >= number in right, and at most 1 more.
            
            # Move from left to right if left has too many active elements
            while len(left) > 0 and len(right) > 0 and (-left[0] > right[0]):
                # This shouldn't happen if we maintain order, but after removals it might.
                # Actually, we maintain that all in left <= all in right.
                # So if top of left > top of right, swap them.
                l_val = -heapq.heappop(left)
                r_val = heapq.heappop(right)
                heapq.heappush(left, -r_val)
                heapq.heappush(right, l_val)
                sum_left = sum_left - l_val + r_val
                sum_right = sum_right - r_val + l_val
            
            # Now balance sizes by moving from left to right or vice versa
            # Count active elements? We can't easily. Instead, we move until the heaps are balanced in terms of total size (including lazy) is not correct.
            # Standard approach: maintain that the number of active elements in left is either equal to or one more than in right.
            # We can track active counts separately.
            pass
        
        # Given the complexity, let's use a simpler O(n * x) approach? No, x can be 10^5.
        # Actually, for the median of a sliding window, a well-known efficient solution uses two heaps with lazy removal.
        # We'll implement it carefully.
        
        # We'll maintain active counts for left and right.
        active_left = 0
        active_right = 0
        
        def add_to_heaps(val):
            nonlocal active_left, active_right, sum_left, sum_right
            if active_left == 0 or val <= -left[0]:
                heapq.heappush(left, -val)
                sum_left += val
                active_left += 1
            else:
                heapq.heappush(right, val)
                sum_right += val
                active_right += 1
            
            # Balance: active_left should be ceil(total/2)
            if active_left > active_right + 1:
                # Move from left to right
                while left and (-left[0] in lazy_left and lazy_left[-left[0]] > 0):
                    v = -heapq.heappop(left)
                    lazy_left[v] -= 1
                    if lazy_left[v] == 0:
                        del lazy_left[v]
                    active_left -= 1
                if left:
                    v = -heapq.heappop(left)
                    active_left -= 1
                    sum_left -= v
                    heapq.heappush(right, v)
                    sum_right += v
                    active_right += 1
            elif active_right > active_left:
                # Move from right to left
                while right and (right[0] in lazy_right and lazy_right[right[0]] > 0):
                    v = heapq.heappop(right)
                    lazy_right[v] -= 1
                    if lazy_right[v] == 0:
                        del lazy_right[v]
                    active_right -= 1
                if right:
                    v = heapq.heappop(right)
                    active_right -= 1
                    sum_right -= v
                    heapq.heappush(left, -v)
                    sum_left += v
                    active_left += 1
        
        def remove_from_heaps(val):
            nonlocal active_left, active_right, sum_left, sum_right
            # Determine which heap val belongs to
            if active_left > 0 and val <= -left[0]:
                # In left
                if val in lazy_left:
                    lazy_left[val] += 1
                else:
                    lazy_left[val] = 1
                sum_left -= val
                active_left -= 1
            else:
                # In right
                if val in lazy_right:
                    lazy_right[val] += 1
                else:
                    lazy_right[val] = 1
                sum_right -= val
                active_right -= 1
        
        # Initialize first window
        for i in range(x):
            add_to_heaps(nums[i])
        
        def get_cost():
            # Clean tops
            while left and (-left[0] in lazy_left and lazy_left[-left[0]] > 0):
                v = -heapq.heappop(left)
                lazy_left[v] -= 1
                if lazy_left[v] == 0:
                    del lazy_left[v]
            while right and (right[0] in lazy_right and lazy_right[right[0]] > 0):
                v = heapq.heappop(right)
                lazy_right[v] -= 1
                if lazy_right[v] == 0:
                    del lazy_right[v]
            
            if not left:
                return 0
            median = -left[0]
            # Cost = (sum_right - sum_left) + median * (active_left - active_right)
            return (sum_right - sum_left) + median * (active_left - active_right)
        
        costs = [0] * n
        costs[x-1] = get_cost()
        
        for i in range(x, n):
            remove_from_heaps(nums[i-x])
            add_to_heaps(nums[i])
            costs[i] = get_cost()
        
        # DP: dp[j] = min operations to have j non-overlapping subarrays
        # We iterate through each ending position of a subarray
        # dp[j] at step i means min cost to have j subarrays using elements up to i
        # But we need to ensure non-overlapping: if a subarray ends at i, the previous one must end at <= i-x
        # So we can use: dp[j] = min over all valid previous ends
        
        # Let dp[j] be the min cost to form j subarrays ending at or before the current position.
        # When we are at index i (end of a window), we can update:
        #   new_dp[j] = min(dp[j], dp[j-1] + costs[i])   if i >= x-1 and j>=1
        # But dp[j-1] should be the best cost for j-1 subarrays ending at or before i-x.
        
        # So we can maintain an array best_prev[j] which is the minimum dp[j] seen so far for indices <= current - x.
        
        INF = float('inf')
        dp = [INF] * (k + 1)
        dp[0] = 0
        
        # best_prev[j] will store the minimum dp[j] for all positions processed so far that are at least x behind the current position
        # We can update best_prev as we go.
        
        # Initialize best_prev with INF, but best_prev[0] = 0 initially (for 0 subarrays, cost 0)
        best_prev = [INF] * (k + 1)
        best_prev[0] = 0
        
        for i in range(n):
            # If we can end a subarray at i (i.e., i >= x-1)
            if i >= x - 1:
                # Update dp for j from k down to 1
                # The previous subarray must end at or before i - x
                # So we use best_prev[j-1] which was updated at step i-x
                for j in range(1, k + 1):
                    if best_prev[j-1] != INF:
                        new_val = best_prev[j-1] + costs[i]
                        if new_val < dp[j]:
                            dp[j] = new_val
                # After processing i, we can update best_prev for future use at i+x
                # But best_prev is updated at the end of the loop for index i, so that at step i+x, best_prev is available.
                # Actually, we should update best_prev[j] with dp[j] after processing i, so that when we are at i+x, best_prev[j] is the min dp[j] for indices <= i.
                for j in range(k + 1):
                    if dp[j] < best_prev[j]:
                        best_prev[j] = dp[j]
            else:
                # For i < x-1, we can't end a subarray, but we still update best_prev for dp[0]
                # dp[0] is always 0, and best_prev[0] is already 0.
                # For j>=1, dp[j] remains INF.
                # But we should update best_prev for j=0? It's already 0.
                # Actually, for i < x-1, we don't have any subarray ending, so dp[j] for j>=1 is INF.
                # We update best_prev[0] = min(best_prev[0], dp[0]) = 0.
                for j in range(k + 1):
                    if dp[j] < best_prev[j]:
                        best_prev[j] = dp[j]
        
        return dp[k] if dp[k] != INF else -1