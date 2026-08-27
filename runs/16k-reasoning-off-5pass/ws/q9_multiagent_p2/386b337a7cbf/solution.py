from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # Constraints analysis:
        # nums.length <= 150, nums[i] <= 12.
        # Max possible alternating sum magnitude: 150 * 12 = 1800.
        # Min possible alternating sum: -1800.
        # We need an offset to map negative sums to positive array indices.
        # Offset 2000 is sufficient to cover [-1800, 1800].
        OFFSET = 2000
        MAX_SUM = 4005  # Covers range roughly [-2000, 2004]
        
        # dp_even[s] stores the maximum product for a subsequence with an EVEN number of elements
        # having an alternating sum of (s - OFFSET).
        # dp_odd[s] stores the maximum product for a subsequence with an ODD number of elements
        # having an alternating sum of (s - OFFSET).
        # Initialize with -1 to represent unreachable states.
        # This initialization naturally handles the "non-empty" requirement because we only
        # populate states by explicitly starting a new subsequence or extending an existing one.
        # The empty subsequence (sum 0, product 1) is never stored, so if we find a valid state
        # with product 1, it must be a non-empty subsequence (e.g., [1] or [1, 1] resulting in sum 0).
        dp_even = [-1] * MAX_SUM
        dp_odd = [-1] * MAX_SUM
        
        # Process each number in nums.
        for x in nums:
            # Create copies to store updates for the current number x.
            # This prevents using the same instance of x multiple times for a single subsequence extension step.
            new_dp_even = dp_even[:]
            new_dp_odd = dp_odd[:]
            
            # Option 1: Start a new subsequence with x.
            # A single element subsequence has length 1 (odd).
            # The alternating sum is just x (index 0 is even, so +x).
            # The next element to be added would be at index 1 (odd), so we subtract.
            if x <= limit:
                idx = x + OFFSET
                if x > new_dp_odd[idx]:
                    new_dp_odd[idx] = x
            
            # Option 2: Extend existing subsequences.
            # We iterate over all possible sums in the current DP tables.
            
            # Extend from a subsequence with EVEN length.
            # The next element (index = even) is ADDED.
            # New length becomes ODD.
            for s in range(MAX_SUM):
                if dp_even[s] != -1:
                    current_prod = dp_even[s]
                    new_sum = s + x
                    if 0 <= new_sum < MAX_SUM:
                        new_prod = current_prod * x
                        if new_prod <= limit:
                            if new_prod > new_dp_odd[new_sum]:
                                new_dp_odd[new_sum] = new_prod
            
            # Extend from a subsequence with ODD length.
            # The next element (index = odd) is SUBTRACTED.
            # New length becomes EVEN.
            for s in range(MAX_SUM):
                if dp_odd[s] != -1:
                    current_prod = dp_odd[s]
                    new_sum = s - x
                    if 0 <= new_sum < MAX_SUM:
                        new_prod = current_prod * x
                        if new_prod <= limit:
                            if new_prod > new_dp_even[new_sum]:
                                new_dp_even[new_sum] = new_prod
            
            # Update the DP tables for the next iteration
            dp_even = new_dp_even
            dp_odd = new_dp_odd
        
        # Check for the target alternating sum k
        target_idx = k + OFFSET
        if 0 <= target_idx < MAX_SUM:
            res_even = dp_even[target_idx]
            res_odd = dp_odd[target_idx]
            
            ans = -1
            if res_even != -1:
                ans = max(ans, res_even)
            if res_odd != -1:
                ans = max(ans, res_odd)
            
            return ans
        
        return -1