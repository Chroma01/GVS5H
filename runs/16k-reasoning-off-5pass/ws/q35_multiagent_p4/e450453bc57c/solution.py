import heapq
from typing import List

class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        
        # Precompute the cost for each window of size x
        # window_costs[i] will store the cost to make nums[i:i+x] uniform
        window_costs = [0] * (n - x + 1)
        
        # Two heaps for sliding window median
        # lo: max-heap (store negative values)
        # hi: min-heap
        lo = []  # max-heap
        hi = []  # min-heap
        
        # Lazy deletion maps
        # We track how many times an element is marked for deletion
        # Since we need to know if the top of the heap is valid, we use a counter
        # But standard lazy deletion uses a separate dict for 'to_remove'
        to_remove = {}
        
        # Sums for cost calculation
        sum_lo = 0
        sum_hi = 0
        
        # Helper to clean up tops of heaps
        def clean_top(heap, is_lo):
            while heap:
                val = heap[0]
                if is_lo:
                    actual_val = -val
                else:
                    actual_val = val
                
                if actual_val in to_remove and to_remove[actual_val] > 0:
                    heapq.heappop(heap)
                    to_remove[actual_val] -= 1
                    if to_remove[actual_val] == 0:
                        del to_remove[actual_val]
                else:
                    break
        
        # Initialize first window
        for i in range(x):
            val = nums[i]
            # Add to lo initially
            heapq.heappush(lo, -val)
            sum_lo += val
            
            # Rebalance: ensure len(lo) >= len(hi) and len(lo) - len(hi) <= 1
            # Actually, for odd x, lo has one more. For even x, they are equal.
            # We maintain: len(lo) == len(hi) or len(lo) == len(hi) + 1
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
        # Median is -lo[0]
        median = -lo[0]
        # Clean tops to ensure median is valid
        clean_top(lo, True)
        clean_top(hi, False)
        median = -lo[0]
        
        cost = sum_lo * (-1) + sum_hi - median * (len(hi) - len(lo))
        # Wait, formula: 
        # Cost = sum(|y - median| for y in window)
        # = sum(median - y for y in lo) + sum(y - median for y in hi)
        # = len(lo)*median - sum_lo + sum_hi - len(hi)*median
        # Note: lo stores negatives, so sum_lo is sum of actual values in lo.
        # But in the heap, we stored -val. So sum_lo should be maintained as sum of actual values.
        # Let's re-verify sum_lo and sum_hi maintenance.
        # When pushing to lo: sum_lo += val (actual val)
        # When popping from lo: sum_lo -= actual_val
        # When pushing to hi: sum_hi += val
        # When popping from hi: sum_hi -= val
        
        # Correct formula:
        # lo has elements <= median, hi has elements >= median.
        # Cost = (median * len(lo) - sum_lo) + (sum_hi - median * len(hi))
        # But note: if len(lo) == len(hi) + 1, median is from lo.
        # If len(lo) == len(hi), median can be from either, but typically we pick -lo[0].
        
        # Let's recalculate cost properly:
        # Clean tops again to be sure
        clean_top(lo, True)
        clean_top(hi, False)
        median = -lo[0]
        
        # len_lo_actual = len(lo) - (number of removed items in lo? No, len(lo) is current heap size)
        # But we need the actual number of valid elements in lo and hi.
        # The heaps might contain deleted items at the top, but we cleaned them.
        # However, deleted items might be buried. 
        # Actually, the standard lazy deletion only cleans the top. 
        # The size of the heap includes deleted items. 
        # This is a problem for maintaining sum_lo and sum_hi correctly if we don't track valid counts.
        
        # Alternative: Instead of maintaining sums incrementally with lazy deletion complexity,
        # given constraints and Python, let's try a simpler approach for cost calculation if N*log(x) is acceptable.
        # N=10^5, x up to 10^5. N*log(x) is ~1.7*10^6 ops. 
        # But calculating cost from scratch is O(x). Total O(N*x) which is too slow.
        
        # Let's stick to the two heaps with lazy deletion but fix the sum tracking.
        # We need to know the number of VALID elements in lo and hi.
        # We can maintain valid_lo_count and valid_hi_count.
        
        # Reset and redo with valid counts
        lo = []
        hi = []
        to_remove = {}
        sum_lo = 0
        sum_hi = 0
        valid_lo_count = 0
        valid_hi_count = 0
        
        def add_to_window(val):
            nonlocal sum_lo, sum_hi, valid_lo_count, valid_hi_count
            # Add to lo
            heapq.heappush(lo, -val)
            sum_lo += val
            valid_lo_count += 1
            
            # Rebalance
            # Move from lo to hi if lo has more valid elements than hi
            if valid_lo_count > valid_hi_count + 1:
                # Pop from lo
                while lo:
                    top = -heapq.heappop(lo)
                    if top in to_remove and to_remove[top] > 0:
                        to_remove[top] -= 1
                        if to_remove[top] == 0:
                            del to_remove[top]
                        continue
                    else:
                        # This is a valid element
                        sum_lo -= top
                        valid_lo_count -= 1
                        heapq.heappush(hi, top)
                        sum_hi += top
                        valid_hi_count += 1
                        break
            elif valid_lo_count < valid_hi_count:
                # Pop from hi
                while hi:
                    top = heapq.heappop(hi)
                    if top in to_remove and to_remove[top] > 0:
                        to_remove[top] -= 1
                        if to_remove[top] == 0:
                            del to_remove[top]
                        continue
                    else:
                        sum_hi -= top
                        valid_hi_count -= 1
                        heapq.heappush(lo, -top)
                        sum_lo += top
                        valid_lo_count += 1
                        break

        def remove_from_window(val):
            nonlocal sum_lo, sum_hi, valid_lo_count, valid_hi_count
            # Mark for removal
            to_remove[val] = to_remove.get(val, 0) + 1
            
            # Adjust sums and counts immediately? 
            # No, lazy deletion means we don't remove from heap immediately.
            # But we must adjust the sums and counts to reflect the removal.
            # However, we don't know which heap the val is in easily without searching.
            # This is the flaw in lazy deletion for sum tracking.
            
            # Better: Don't use lazy deletion for sum tracking. 
            # Use a balanced BST simulation or just recalculate cost if x is small?
            # Given k is small, maybe we can optimize differently.
            
            # Actually, for competitive programming in Python, a common trick for sliding window median cost:
            # Use the fact that we only need the median. 
            # We can use a sorted list and bisect? O(x) per window -> O(N*x) total. Too slow.
            
            # Let's use the two heaps with lazy deletion, but handle sums carefully.
            # When removing, we don't know which heap it's in. 
            # We can check: if val <= median, it's in lo, else in hi.
            # But median changes. 
            # Standard approach: 
            # Maintain balance. When removing, if val <= current median, it should be in lo.
            # But current median might not be accurate if tops are dirty.
            
            # Given the complexity, and that k is small, let's try a different DP state or optimization.
            # Actually, the constraints allow O(N * k) if cost calculation is O(1) or O(log x).
            
            # Let's implement a simpler cost calculation: 
            # Since x is fixed, we can use a Fenwick tree or Segment Tree over the values? 
            # Values are in [-10^6, 10^6]. Coordinate compression + Fenwick tree for rank and sum.
            # This allows finding median and sum of absolute differences in O(log M).
            # M = 2*10^6 + 1. 
            # This is robust.
            
            pass

        # Given the time, I will implement the Fenwick Tree approach for sliding window median cost.
        # It's O(N log M) which is efficient.
        
        # Coordinate compression
        all_vals = sorted(set(nums))
        val_to_idx = {v: i+1 for i, v in enumerate(all_vals)}
        m = len(all_vals)
        
        # Fenwick Tree for count and sum
        bit_count = [0] * (m + 1)
        bit_sum = [0] * (m + 1)
        
        def update(idx, delta_count, delta_sum):
            while idx <= m:
                bit_count[idx] += delta_count
                bit_sum[idx] += delta_sum
                idx += idx & (-idx)
                
        def query_count(idx):
            res = 0
            while idx > 0:
                res += bit_count[idx]
                idx -= idx & (-idx)
            return res
                
        def query_sum(idx):
            res = 0
            while idx > 0:
                res += bit_sum[idx]
                idx -= idx & (-idx)
            return res
        
        # Find k-th smallest element index
        def find_kth(k):
            idx = 0
            bit_mask = 1
            while bit_mask <= m:
                bit_mask <<= 1
            bit_mask >>= 1
            
            current_idx = 0
            current_count = 0
            while bit_mask > 0:
                next_idx = current_idx + bit_mask
                if next_idx <= m and current_count + bit_count[next_idx] < k:
                    current_idx = next_idx
                    current_count += bit_count[next_idx]
                bit_mask >>= 1
            return current_idx + 1
        
        # Initialize first window
        for i in range(x):
            val = nums[i]
            idx = val_to_idx[val]
            update(idx, 1, val)
            
        # Calculate cost for first window
        # Median is the (x+1)//2 -th smallest element
        kth = (x + 1) // 2
        median_idx = find_kth(kth)
        median = all_vals[median_idx - 1]
        
        # Cost = sum(|num - median|)
        # = sum(num > median ? num - median : median - num)
        # = (sum of elements > median) - (count of elements > median) * median 
        #   + (count of elements <= median) * median - (sum of elements <= median)
        
        count_le = query_count(median_idx)
        sum_le = query_sum(median_idx)
        count_gt = x - count_le
        sum_gt = x * median - sum_le # Wait, total sum is not x*median. Total sum is query_sum(m).
        total_sum = query_sum(m)
        sum_gt = total_sum - sum_le
        
        cost = (sum_gt - count_gt * median) + (count_le * median - sum_le)
        window_costs[0] = cost
        
        # Slide window
        for i in range(1, n - x + 1):
            # Remove nums[i-1]
            val_out = nums[i-1]
            idx_out = val_to_idx[val_out]
            update(idx_out, -1, -val_out)
            
            # Add nums[i+x-1]
            val_in = nums[i+x-1]
            idx_in = val_to_idx[val_in]
            update(idx_in, 1, val_in)
            
            # Find new median
            median_idx = find_kth(kth)
            median = all_vals[median_idx - 1]
            
            count_le = query_count(median_idx)
            sum_le = query_sum(median_idx)
            total_sum = query_sum(m)
            count_gt = x - count_le
            sum_gt = total_sum - sum_le
            
            cost = (sum_gt - count_gt * median) + (count_le * median - sum_le)
            window_costs[i] = cost
            
        # DP
        # dp[j][i] = min cost to have j subarrays using prefix nums[0...i-1]
        # dp[j][i] = min(dp[j][i-1], dp[j-1][i-x] + window_costs[i-x])
        
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(k + 1)]
        
        for i in range(n + 1):
            dp[0][i] = 0
            
        for j in range(1, k + 1):
            for i in range(1, n + 1):
                # Option 1: Skip element i-1
                dp[j][i] = dp[j][i-1]
                
                # Option 2: End a subarray at i-1 (window ends at i-1, starts at i-x)
                if i >= x:
                    prev = dp[j-1][i-x]
                    if prev != INF:
                        current_cost = window_costs[i-x]
                        if prev + current_cost < dp[j][i]:
                            dp[j][i] = prev + current_cost
                            
        return dp[k][n]