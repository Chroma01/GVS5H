class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        left = 0
        total_count = 0
        current_cost = 0
        # adjusted[i] will store the adjusted value of nums[i] in the current window
        # We only need to store adjusted values for the current window
        adjusted = []
        
        for right in range(n):
            # Add nums[right] to the window
            if not adjusted:
                new_adj = nums[right]
            else:
                prev_adj = adjusted[-1]
                new_adj = max(nums[right], prev_adj)
            
            current_cost += new_adj - nums[right]
            adjusted.append(new_adj)
            
            # If cost exceeds k, shrink from the left
            while current_cost > k and left <= right:
                # Remove nums[left]
                # We need to recompute the adjusted values for the window [left+1, right]
                # This is O(window_size) in the worst case
                
                if left == right:
                    adjusted = []
                    current_cost = 0
                    left += 1
                    break
                
                # Check if we can avoid full recomputation
                # If nums[left+1] >= adjusted[0], then adjusted[1] was nums[left+1]
                # and the rest of the adjusted values are unchanged.
                if nums[left+1] >= adjusted[0]:
                    adjusted.pop(0)
                    # The cost for nums[left+1] was 0, so no change to current_cost
                else:
                    # nums[left+1] < adjusted[0]
                    # adjusted[1] was adjusted[0]. Now it becomes nums[left+1].
                    # We need to recompute the rest.
                    new_adjusted = [nums[left+1]]
                    new_cost = 0
                    for i in range(left+2, right+1):
                        prev = new_adjusted[-1]
                        curr = nums[i]
                        adj = max(curr, prev)
                        new_cost += adj - curr
                        new_adjusted.append(adj)
                    current_cost = new_cost
                    adjusted = new_adjusted
                
                left += 1
            
            # All subarrays ending at right and starting from left to right are valid
            total_count += (right - left + 1)
        
        return total_count