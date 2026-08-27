import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # dp[j] will store the minimum cost to form exactly j non-overlapping subarrays
        # using a prefix of the array processed so far.
        # Initialize with infinity, except dp[0] = 0.
        dp = [float('inf')] * (k + 1)
        dp[0] = 0
        
        # We need to efficiently calculate the cost to make a subarray of length x ending at i
        # have equal elements. The optimal target value is the median of the subarray.
        # We use two heaps to maintain the median of the current window of size x.
        # left_heap: max-heap (stores negative values) for the lower half
        # right_heap: min-heap for the upper half
        left_heap = []
        right_heap = []
        
        # To maintain the sum of absolute differences from the median, we track:
        # sum_left: sum of elements in left_heap
        # sum_right: sum of elements in right_heap
        # sum_left_neg: sum of (-val) for val in left_heap (to handle max-heap logic easily)
        # Actually, let's just track sum of actual values in heaps.
        sum_left = 0
        sum_right = 0
        
        # We iterate through the array. We only start forming subarrays once we have at least x elements.
        # However, we need to slide the window.
        # Let's maintain the window [i-x+1, i].
        
        for i in range(n):
            val = nums[i]
            
            # Add current value to the heaps
            if not left_heap or val <= -left_heap[0]:
                heapq.heappush(left_heap, -val)
                sum_left += val
            else:
                heapq.heappush(right_heap, val)
                sum_right += val
            
            # Balance heaps: left_heap should have size ceil(x/2) or floor?
            # For median definition in cost minimization (sum of abs diffs), any median works.
            # Usually, we balance such that len(left) == len(right) or len(left) == len(right) + 1.
            # Let's enforce: len(left) >= len(right) and len(left) - len(right) <= 1.
            while len(left_heap) > len(right_heap) + 1:
                moved = -heapq.heappop(left_heap)
                sum_left -= moved
                heapq.heappush(right_heap, moved)
                sum_right += moved
            
            while len(right_heap) > len(left_heap):
                moved = heapq.heappop(right_heap)
                sum_right -= moved
                heapq.heappush(left_heap, -moved)
                sum_left += moved
            
            # If we have a full window of size x
            if i >= x - 1:
                # Remove the element leaving the window: nums[i-x]
                leaving = nums[i - x]
                
                # Determine which heap the leaving element is in
                # We need to know if leaving was in left or right.
                # Since we don't store history, we check against current median logic.
                # But the heaps might have changed since 'leaving' was added.
                # However, we can deduce: if leaving <= current_median, it's likely in left.
                # But strictly, we need to find it.
                # Alternative: Re-insertion logic is complex.
                # Better approach: Since x is fixed, we can just re-calculate the cost?
                # No, O(x) per step is too slow if x is large.
                # We must remove efficiently.
                
                # Let's refine the heap management to track membership or use a different structure.
                # Actually, for the median cost, we can use a simpler property:
                # Cost = (sum of elements > median) - (sum of elements < median) + (count_diff * median) ?
                # No, Cost = sum(|a - m|).
                # If we maintain the heaps correctly, we can find the leaving element by checking
                # if it is <= -left_heap[0] (current median candidate).
                # But the heaps are dynamic.
                
                # Correct removal strategy:
                # 1. Check if leaving <= -left_heap[0]. If so, it must be in left_heap.
                #    But wait, -left_heap[0] is the max of the lower half.
                #    If leaving <= max_lower, it is in lower half.
                #    However, there might be duplicates. We just need to remove one instance.
                # 2. If leaving > -left_heap[0], it is in right_heap.
                
                # Is this logic sound?
                # The invariant is: all elements in left_heap <= all elements in right_heap.
                # So if leaving <= max(left_heap), it is in left_heap.
                # If leaving > max(left_heap), it is in right_heap.
                # This holds true regardless of duplicates because the split is strict.
                
                median = -left_heap[0]
                
                if leaving <= median:
                    # Remove from left_heap
                    # We need to find and remove 'leaving'. Since it's a heap, we can't remove by value directly.
                    # We can use a lazy removal approach or just rebuild?
                    # Rebuilding is O(x log x) which is too slow if done every step.
                    # Lazy removal: mark as removed.
                    # But we need to know the sum.
                    
                    # Let's use a different approach for the sliding window median cost.
                    # Since k is small, maybe we don't need the median for every window?
                    # No, we need the cost for every potential subarray ending at i to update DP.
                    
                    # Let's implement lazy removal.
                    # We maintain the heaps and a "to_remove" set/dict.
                    # When popping, if the top is in to_remove, pop and discard.
                    # But we also need to update sums.
                    # This is tricky because we need to know the value to subtract from sum.
                    
                    # Alternative: Since x <= 10^5, but n <= 10^5, O(n log x) is fine.
                    # The issue is removing an arbitrary element from a heap.
                    # We can use a "heap with lazy deletion" but we need to track the sum.
                    # We can store (value, index) in heaps? No, values are not unique.
                    
                    # Let's reconsider the problem constraints and properties.
                    # Is there a way to avoid explicit removal?
                    # Maybe we can just recompute the cost for the window?
                    # If x is small, yes. If x is large, no.
                    # But note: we only need to update DP when we have a valid window.
                    # The number of windows is n.
                    
                    # Let's try the lazy removal with a counter for each value?
                    # No, values can be large.
                    # How about we just use a balanced BST? Python doesn't have one in stdlib.
                    
                    # Wait, we can use the property that we only need the median and the sum of abs diffs.
                    # Let's maintain the heaps and the sums.
                    # When removing 'leaving':
                    # If leaving <= median:
                    #   We assume it's in left_heap. But we don't know which one.
                    #   However, we can just pop from left_heap until we find 'leaving'?
                    #   That could be O(x) in worst case.
                    
                    # Is there a better way?
                    # Yes, we can use two heaps and a "lazy" set of removed elements.
                    # But we need to update the sum.
                    # We can store the sum of elements currently in the heap (excluding lazy removed ones).
                    # When we need to remove 'leaving':
                    #   If leaving <= median:
                    #       We know it's in the left part. But we don't know its position.
                    #       We can't easily remove it.
                    
                    # Let's step back.
                    # Maybe we can iterate backwards? No.
                    
                    # What if we use a Fenwick tree or Segment Tree over the values?
                    # Values are in range [-10^6, 10^6]. We can shift them to [0, 2*10^6].
                    # A segment tree can maintain:
                    #   - count of numbers
                    #   - sum of numbers
                    #   - sum of absolute differences from median?
                    #   Actually, with a segment tree, we can find the median in O(log M) and calculate the cost in O(log M).
                    #   M = 2*10^6 + 1.
                    #   Operations: add, remove, query median, query cost.
                    #   This is O(n log M). With n=10^5, log M ~ 21. Total ops ~ 2*10^6. Very fast.
                    
                    # Let's implement the Segment Tree approach.
                    # Range: [-10^6, 10^6]. Offset by 10^6 -> [0, 2*10^6].
                    # Size of tree: 2^21 = 2097152.
                    
                    # Segment Tree Node:
                    #   count: number of elements in range
                    #   total_sum: sum of elements in range
                    # We can compute cost as:
                    #   Find median m (the k-th element where k = count/2).
                    #   Cost = sum_{v > m} (v - m) + sum_{v < m} (m - v)
                    #        = (sum_{v > m} v - count_{v > m} * m) + (count_{v < m} * m - sum_{v < m} v)
                    #        = (total_sum_right - count_right * m) + (count_left * m - total_sum_left)
                    # We can query prefix sums and counts from the segment tree.
                    
                    pass
                
                # Re-implementing with Segment Tree logic inside the loop.
                # But wait, the problem asks for a class method. We can define a helper class or functions.
                # Given the constraints and Python, a Segment Tree is feasible and robust.
                
                # Let's define the Segment Tree.
                # Range [0, 2000000].
                # We need:
                #   update(index, delta_count, delta_sum)
                #   query_count(index) -> returns count in [0, index]
                #   query_sum(index) -> returns sum in [0, index]
                #   find_kth(k) -> returns the value v such that count in [0, v] >= k and count in [0, v-1] < k.
                
                # Actually, we can just maintain the tree and do these operations.
                # Since we need to do this for every i, and n=10^5, O(n log M) is perfect.
                
                # Let's write the Segment Tree implementation.
                # To save space and time, we can use an array-based implementation.
                # Size: 4 * 2000000 is too big (8 million ints). It's about 32MB, which is fine.
                # But we need two arrays: one for count, one for sum.
                
                # Let's refine the range.
                # Min value: -10^6, Max value: 10^6.
                # Offset: 10^6.
                # Range: 0 to 2000000.
                # Tree size: 2^21 = 2097152.
                # We need 2 * 2^21 integers. ~4 million ints. ~16MB. Very safe.
                
                # Implementation details:
                # tree_count[node] stores count of numbers in the range covered by node.
                # tree_sum[node] stores sum of numbers in the range covered by node.
                # Leaf node at index 'idx' (representing value 'idx - offset') will have:
                #   count = 1 if nums[i] == idx-offset else 0
                #   sum = nums[i] if nums[i] == idx-offset else 0
                # But we are adding/removing one by one.
                
                # We will use a recursive or iterative segment tree. Iterative is faster and simpler.
                # Size N = 2097152.
                # Tree array size 2*N.
                
                # Let's code this.
                
                # Wait, I need to integrate this into the existing loop structure.
                # I will replace the heap logic with the segment tree logic.
                
                # Re-writing the solution with Segment Tree.
                pass
        
        # Let's restart the code block with the Segment Tree solution.
        pass

    # Redefining the method with Segment Tree
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        # dp[j] = min cost to form j subarrays
        dp = [float('inf')] * (k + 1)
        dp[0] = 0
        
        # Segment Tree setup
        # Range: [-10^6, 10^6] -> [0, 2000000]
        OFFSET = 1000000
        MAX_VAL = 2000000
        size = 1
        while size <= MAX_VAL:
            size *= 2
        
        tree_count = [0] * (2 * size)
        tree_sum = [0] * (2 * size)
        
        def update(pos, val):
            # pos is the value in [0, MAX_VAL]
            idx = pos + size
            tree_count[idx] += val
            tree_sum[idx] += val * val  # Wait, we need sum of values, not squares.
            # Correction: tree_sum stores sum of values.
            # But to calculate cost, we need sum of values.
            # Let's store sum of values.
            # tree_sum[idx] += val
            # But wait, if we add 'val' multiple times, we need to track count and sum.
            # Actually, we are adding/removing one instance of 'val'.
            # So:
            # tree_count[idx] += 1 (for add) or -= 1 (for remove)
            # tree_sum[idx] += val (for add) or -= val (for remove)
            # But the function signature is update(pos, val) where val is +1 or -1.
            # Let's adjust.
            pass
        
        # Let's rewrite the update function properly.
        # We need to support: add(val), remove(val).
        # val is the actual number.
        # We map val to idx = val + OFFSET.
        
        # We need to find the median.
        # The median is the element at rank (total_count // 2) or similar.
        # Since we want to minimize sum of absolute differences, any median works.
        # Usually, if total_count is odd, median is the middle element.
        # If even, any value between the two middle elements works.
        # We can pick the element at rank (total_count + 1) // 2 (1-based) or total_count // 2 (0-based).
        # Let's use 0-based rank: we want the element at index total_count // 2 in the sorted list.
        
        # To find the k-th element (0-based) in O(log M):
        # Traverse the tree.
        # If left_child.count > k: go left.
        # Else: k -= left_child.count, go right.
        
        # To calculate cost given median m:
        # Cost = (sum of elements > m) - (count of elements > m) * m + (count of elements < m) * m - (sum of elements < m)
        # We can get sum and count for [0, m-1] and [m+1, MAX_VAL] using prefix queries.
        # But our tree is built on indices.
        # We can query range [0, m-1] and [m+1, MAX_VAL].
        # Or simply:
        # total_count = tree_count[root]
        # total_sum = tree_sum[root]
        # count_left = query_count(0, m-1)
        # sum_left = query_sum(0, m-1)
        # count_right = total_count - count_left - (1 if m exists else 0)
        # sum_right = total_sum - sum_left - (m if m exists else 0)
        # But we need to know if m exists.
        # Actually, if we pick m as the median value, it must exist in the array (since we pick an element from the array).
        # So count at m is >= 1.
        # Cost = (sum_right - count_right * m) + (count_left * m - sum_left)
        
        # Let's implement the Segment Tree with iterative approach for speed.
        
        # Arrays
        # size is power of 2 >= 2000001.
        # tree_count, tree_sum
        
        # Helper to query range [l, r] inclusive
        def query_count(l, r):
            if l > r: return 0
            l += size
            r += size
            res = 0
            while l <= r:
                if l % 2 == 1:
                    res += tree_count[l]
                    l += 1
                if r % 2 == 0:
                    res += tree_count[r]
                    r -= 1
                l //= 2
                r //= 2
            return res
        
        def query_sum(l, r):
            if l > r: return 0
            l += size
            r += size
            res = 0
            while l <= r:
                if l % 2 == 1:
                    res += tree_sum[l]
                    l += 1
                if r % 2 == 0:
                    res += tree_sum[r]
                    r -= 1
                l //= 2
                r //= 2
            return res
        
        # Find k-th element (0-based)
        def find_kth(k):
            # k is 0-based index in the sorted sequence of elements currently in the tree.
            # We want the element at index k.
            node = 1
            curr_count = tree_count[node]
            if k >= curr_count:
                return -1 # Should not happen
            while node < size:
                left_count = tree_count[2 * node]
                if k < left_count:
                    node = 2 * node
                else:
                    k -= left_count
                    node = 2 * node + 1
            return node - size
        
        # Update: add or remove a value
        def update(val, delta):
            idx = val + OFFSET
            idx += size
            tree_count[idx] += delta
            tree_sum[idx] += delta * val
            idx //= 2
            while idx > 0:
                tree_count[idx] = tree_count[2 * idx] + tree_count[2 * idx + 1]
                tree_sum[idx] = tree_sum[2 * idx] + tree_sum[2 * idx + 1]
                idx //= 2
        
        # Initialize
        # We will process the array and maintain the window.
        # We need to add nums[i] and remove nums[i-x] when i >= x.
        
        # But wait, we need to calculate the cost for the window ending at i.
        # The window is [i-x+1, i].
        # We add nums[i] first, then if i >= x, we remove nums[i-x] and calculate cost.
        
        for i in range(n):
            val = nums[i]
            update(val, 1)
            
            if i >= x:
                leaving = nums[i - x]
                update(leaving, -1)
                
                # Calculate cost for the current window
                total_count = tree_count[1]
                if total_count == 0:
                    continue
                
                # Find median
                # For sum of absolute differences, any median works.
                # We pick the element at rank total_count // 2 (0-based).
                median_val = find_kth(total_count // 2)
                
                # Calculate cost
                # Cost = sum(|v - median|)
                # = (sum of v > median) - (count of v > median) * median + (count of v < median) * median - (sum of v < median)
                
                # Count and sum for [0, median_val - 1]
                count_left = query_count(0, median_val + OFFSET - 1)
                sum_left = query_sum(0, median_val + OFFSET - 1)
                
                # Count and sum for [median_val + 1, MAX_VAL]
                count_right = query_count(median_val + OFFSET + 1, MAX_VAL)
                sum_right = query_sum(median_val + OFFSET + 1, MAX_VAL)
                
                # Note: elements equal to median_val are not included in left or right, which is correct.
                # Their contribution to cost is 0.
                
                cost = (sum_right - count_right * median_val) + (count_left * median_val - sum_left)
                
                # Update DP
                # We can form j subarrays ending at i if we had j-1 subarrays before.
                # We iterate j from k down to 1.
                for j in range(k, 0, -1):
                    if dp[j-1] != float('inf'):
                        if dp[j-1] + cost < dp[j]:
                            dp[j] = dp[j-1] + cost
        
        return dp[k]