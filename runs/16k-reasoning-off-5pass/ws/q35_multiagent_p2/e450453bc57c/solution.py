import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # cost[i] will store the cost to make nums[i:i+x] all equal
        cost = [0] * (n - x + 1)
        
        # Two heaps for median maintenance:
        # lo: max-heap (store negative values) for the lower half
        # hi: min-heap for the upper half
        lo = []  # max-heap
        hi = []  # min-heap
        sum_lo = 0
        sum_hi = 0
        
        # Initialize the first window
        for i in range(x):
            val = nums[i]
            # Add to lo initially
            heapq.heappush(lo, -val)
            sum_lo += val
            # Balance: ensure lo has one more or equal to hi
            if len(lo) > len(hi) + 1:
                moved = -heapq.heappop(lo)
                sum_lo -= moved
                heapq.heappush(hi, moved)
                sum_hi += moved
            elif len(lo) < len(hi):
                moved = heapq.heappop(hi)
                sum_hi -= moved
                heapq.heappush(lo, -moved)
                sum_lo += moved
        
        # Calculate cost for first window
        median = -lo[0]
        # Cost = sum(|val - median|) for val in window
        # = (sum_lo_adjusted) + (sum_hi_adjusted)
        # where sum_lo_adjusted = median * len(lo) - sum_lo
        #       sum_hi_adjusted = sum_hi - median * len(hi)
        # But note: if median is from lo, then for elements in lo, |val - median| = median - val
        # For elements in hi, |val - median| = val - median
        # However, if there are duplicates or median appears in both, the formula still holds if we consider the heaps partition correctly.
        # Actually, a simpler way: 
        # cost = (sum of elements in hi) - (sum of elements in lo) + (if median is in lo and size diff, adjust?)
        # Standard formula: 
        # Let L be the sum of the lower half, R be the sum of the upper half.
        # Let m be the median.
        # Cost = (m * len(lo) - L) + (R - m * len(hi))
        # But if the median is taken from lo, then the element at the top of lo is m.
        # The above formula works if we define lo and hi such that all elements in lo <= all elements in hi.
        
        # Recalculate cost properly:
        # We have maintained that len(lo) == len(hi) or len(lo) == len(hi) + 1.
        # The median is -lo[0].
        # The cost is sum(|v - median| for v in window).
        # We can compute it as:
        #   cost = (sum_hi - median * len(hi)) + (median * len(lo) - sum_lo)
        # But note: sum_lo includes the median if it's in lo.
        # This formula is correct.
        current_cost = (sum_hi - median * len(hi)) + (median * len(lo) - sum_lo)
        cost[0] = current_cost
        
        # Helper to add a new element to the heaps
        def add(val):
            nonlocal sum_lo, sum_hi
            # Add to lo first
            heapq.heappush(lo, -val)
            sum_lo += val
            # Balance heaps
            if len(lo) > len(hi) + 1:
                moved = -heapq.heappop(lo)
                sum_lo -= moved
                heapq.heappush(hi, moved)
                sum_hi += moved
            elif len(lo) < len(hi):
                moved = heapq.heappop(hi)
                sum_hi -= moved
                heapq.heappush(lo, -moved)
                sum_lo += moved
        
        # Helper to remove an old element from the heaps (lazy removal not used here, we rebuild? No, that's O(x) per step -> O(n*x) which is too slow if x is large)
        # Actually, with x up to 10^5, O(n*x) is TLE.
        # We need a way to remove from heaps. Since we slide one by one, we can use lazy removal.
        # But lazy removal with two heaps for median is tricky because we need to know the current median and sums.
        # Alternative: Use a balanced BST simulation? In Python, we don't have one.
        # Another approach: Since x is fixed, we can use a segment tree or sqrt decomposition? 
        # Actually, a common technique for sliding window median is to use two heaps with lazy removal.
        # We maintain counts of elements to be removed.
        
        # Let's restart the precomputation with lazy removal.
        lo = []
        hi = []
        sum_lo = 0
        sum_hi = 0
        # To handle lazy removal, we keep track of elements that are "logically" removed.
        # But we also need to maintain the sums correctly.
        # We'll use dictionaries to count removed elements.
        lo_removed = {}
        hi_removed = {}
        
        def clean_lo():
            nonlocal sum_lo
            while lo and (-lo[0]) in lo_removed and lo_removed[-lo[0]] > 0:
                val = -heapq.heappop(lo)
                lo_removed[val] -= 1
                if lo_removed[val] == 0:
                    del lo_removed[val]
                # Note: we don't adjust sum_lo here because the element was already subtracted when it was logically removed? 
                # Actually, we need to adjust sum_lo when we remove from lo.
                # This is complex. Let's use a different method: 
                # Instead of lazy removal, since x is fixed, we can just rebuild the heaps for each window? 
                # That would be O(n * x log x) which is too slow.
                
        # Given the constraints and complexity of lazy removal with sums, 
        # and knowing that k is small (<=15), but n is 10^5, 
        # we need an efficient O(n log x) or O(n) method.
        
        # Alternative efficient method for sliding window median cost:
        # Use a Fenwick tree or Segment Tree over the values? 
        # Values are in [-10^6, 10^6], so we can compress them.
        # But implementing a segment tree for median and sum of absolute differences is complex.
        
        # Let's try the two heaps with lazy removal carefully.
        # We maintain:
        #   lo: max-heap of the lower half
        #   hi: min-heap of the upper half
        #   sum_lo: sum of elements in lo (including those marked for removal? No, we adjust sums on removal)
        #   sum_hi: sum of elements in hi
        #   We also maintain the actual size of lo and hi (logical size).
        
        # Reset
        lo = []
        hi = []
        sum_lo = 0
        sum_hi = 0
        lo_removed = {}
        hi_removed = {}
        lo_size = 0
        hi_size = 0
        
        def push(val):
            nonlocal sum_lo, sum_hi, lo_size, hi_size
            if lo_size == 0 or val <= -lo[0]:
                heapq.heappush(lo, -val)
                sum_lo += val
                lo_size += 1
            else:
                heapq.heappush(hi, val)
                sum_hi += val
                hi_size += 1
            balance()
            
        def remove(val):
            nonlocal sum_lo, sum_hi, lo_size, hi_size
            # Determine which heap the val belongs to
            if lo_size > 0 and val <= -lo[0]:
                # It should be in lo
                if val in lo_removed:
                    lo_removed[val] += 1
                else:
                    lo_removed[val] = 1
                sum_lo -= val
                lo_size -= 1
            else:
                if val in hi_removed:
                    hi_removed[val] += 1
                else:
                    hi_removed[val] = 1
                sum_hi -= val
                hi_size -= 1
            balance()
            
        def balance():
            nonlocal sum_lo, sum_hi
            # We want lo_size == hi_size or lo_size == hi_size + 1
            while lo_size > hi_size + 1:
                # Move from lo to hi
                while lo and (-lo[0]) in lo_removed and lo_removed[-lo[0]] > 0:
                    v = -heapq.heappop(lo)
                    lo_removed[v] -= 1
                    if lo_removed[v] == 0:
                        del lo_removed[v]
                if lo:
                    v = -heapq.heappop(lo)
                    sum_lo -= v
                    lo_size -= 1
                    heapq.heappush(hi, v)
                    sum_hi += v
                    hi_size += 1
                else:
                    break
            while hi_size > lo_size:
                while hi and hi[0] in hi_removed and hi_removed[hi[0]] > 0:
                    v = heapq.heappop(hi)
                    hi_removed[v] -= 1
                    if hi_removed[v] == 0:
                        del hi_removed[v]
                if hi:
                    v = heapq.heappop(hi)
                    sum_hi -= v
                    hi_size -= 1
                    heapq.heappush(lo, -v)
                    sum_lo += v
                    lo_size += 1
                else:
                    break
                    
        def get_median():
            # Clean tops
            while lo and (-lo[0]) in lo_removed and lo_removed[-lo[0]] > 0:
                v = -heapq.heappop(lo)
                lo_removed[v] -= 1
                if lo_removed[v] == 0:
                    del lo_removed[v]
            return -lo[0]
            
        # Initialize first window
        for i in range(x):
            push(nums[i])
            
        median = get_median()
        # Cost calculation
        # Cost = (sum_hi - median * hi_size) + (median * lo_size - sum_lo)
        current_cost = (sum_hi - median * hi_size) + (median * lo_size - sum_lo)
        cost[0] = current_cost
        
        # Slide the window
        for i in range(1, n - x + 1):
            # Remove nums[i-1]
            remove(nums[i-1])
            # Add nums[i+x-1]
            push(nums[i+x-1])
            
            median = get_median()
            current_cost = (sum_hi - median * hi_size) + (median * lo_size - sum_lo)
            cost[i] = current_cost
            
        # DP
        # dp[j][i] = min cost to have j subarrays using first i elements (indices 0 to i-1)
        # Dimensions: (k+1) x (n+1)
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        for i in range(n + 1):
            dp[0][i] = 0
            
        for j in range(1, k + 1):
            for i in range(1, n + 1):
                # Option 1: Skip the i-th element (index i-1) as the end of a subarray
                dp[j][i] = dp[j][i-1]
                # Option 2: Form a subarray ending at index i-1 (starting at i-x)
                if i >= x:
                    prev = dp[j-1][i-x]
                    if prev != INF:
                        c = cost[i-x]
                        if prev + c < dp[j][i]:
                            dp[j][i] = prev + c
                            
        return dp[k][n]