class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        count = 0
        
        # We use a two-pointer (sliding window) approach.
        # For each right, we maintain the smallest left such that the cost to make nums[left..right] non-decreasing is <= k.
        # The cost is calculated greedily: iterate from left to right, keeping track of the current maximum (adjusted) value.
        # If nums[i] < current_max, we need (current_max - nums[i]) operations to raise nums[i] to current_max.
        # The current_max remains unchanged. If nums[i] >= current_max, current_max becomes nums[i].
        
        # To optimize, we maintain the adjusted values and current cost incrementally when expanding right.
        # When shrinking left, we recompute the adjusted values and cost for the new window.
        # Although recomputation is O(window_size), in practice, the window size is often small, or the cost is 0.
        # For worst-case scenarios (e.g., strictly decreasing array with small k), the window size is small, so it's efficient.
        
        left = 0
        # adj[i] will store the adjusted value of nums[left + i] for the current window [left, right]
        adj = []  
        current_cost = 0
        
        for right in range(n):
            # Expand the window to include nums[right]
            if not adj:
                # First element in the window
                adj.append(nums[right])
                current_cost = 0
            else:
                # The adjusted value of the previous element is adj[-1]
                prev_adj = adj[-1]
                if nums[right] < prev_adj:
                    current_cost += prev_adj - nums[right]
                    adj.append(prev_adj)
                else:
                    adj.append(nums[right])
            
            # If cost exceeds k, shrink from the left
            while current_cost > k:
                # Remove the leftmost element
                left += 1
                if left > right:
                    # Window is empty, reset
                    adj = []
                    current_cost = 0
                    break
                
                # Recompute adjusted values for the new window [left, right]
                # This is O(window_size)
                adj = [nums[left]]
                current_cost = 0
                for i in range(left + 1, right + 1):
                    prev_adj = adj[-1]
                    if nums[i] < prev_adj:
                        current_cost += prev_adj - nums[i]
                        adj.append(prev_adj)
                    else:
                        adj.append(nums[i])
                    # Early termination if cost exceeds k
                    if current_cost > k:
                        break
            
            # Add the number of valid subarrays ending at right
            # All subarrays nums[left..right], nums[left+1..right], ..., nums[right..right] are valid
            count += (right - left + 1)
            
        return count