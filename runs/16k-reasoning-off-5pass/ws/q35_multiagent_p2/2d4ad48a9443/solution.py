class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        result = 0
        l = 0
        # We'll maintain a stack of indices where the floor value changes.
        # The stack will store indices i such that nums[i] is a new floor (i.e., nums[i] > previous floor).
        # We also maintain the current cost for the window [l, r].
        
        # Instead of a full recalculation, we can use a different approach:
        # For each r, we want to find the smallest l such that cost(l, r) <= k.
        # We can compute the cost for [l, r] by simulating the greedy pass.
        # To do this efficiently, we note that when we move r to r+1, we add one element.
        # When we move l to l+1, we remove one element, which might change the floor for subsequent elements.
        
        # Given the complexity of maintaining the cost incrementally with a stack, 
        # and since n is up to 10^5, we use a two-pointer with a naive cost calculation but with early termination.
        # However, worst-case O(n^2) might be too slow. 
        # 
        # Alternative efficient approach:
        # Use a segment tree or a deque to maintain the cost. But implementing that is complex.
        #
        # We'll use a two-pointer with a naive cost calculation, but optimize by breaking early.
        # In practice, the window size might be small on average.
        
        # Let's implement a clean two-pointer with full recalculation but with a while loop for l.
        # To avoid O(n^2), we note that each element is added and removed at most once? 
        # No, because cost recalculation is O(window_size).
        
        # Given the constraints, we'll implement the following:
        # For each r, we start with the current l. If the window [l, r] is invalid, we increment l and recalculate cost until valid or l > r.
        
        # We'll compute cost for [l, r] from scratch.
        # To optimize, we can break early in the cost calculation.
        
        # We'll use a list to store the current window's elements? No, we just use indices.
        
        # Initialize result
        result = 0
        l = 0
        for r in range(n):
            # Calculate cost for window [l, r]
            # Start from l
            floor_val = nums[l]
            current_cost = 0
            valid = True
            for i in range(l + 1, r + 1):
                if nums[i] < floor_val:
                    current_cost += floor_val - nums[i]
                    # floor_val remains the same because we incremented nums[i] to floor_val
                else:
                    floor_val = nums[i]
                if current_cost > k:
                    valid = False
                    break
            
            if valid:
                result += r - l + 1
            else:
                # Move l forward until the window becomes valid or l > r
                while l < r:
                    l += 1
                    if l > r:
                        break
                    floor_val = nums[l]
                    current_cost = 0
                    for i in range(l + 1, r + 1):
                        if nums[i] < floor_val:
                            current_cost += floor_val - nums[i]
                        else:
                            floor_val = nums[i]
                        if current_cost > k:
                            break
                    else:
                        # If the loop completed without breaking, the window is valid.
                        valid = True
                        break
                
                if valid:
                    result += r - l + 1
                # else: no valid window ends at r, so add 0.
        
        return result