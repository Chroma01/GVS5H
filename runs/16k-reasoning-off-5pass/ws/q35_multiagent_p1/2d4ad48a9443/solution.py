class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # diff[i] = max(0, nums[i-1] - nums[i]) for i > 0, diff[0] = 0
        # The cost for subarray nums[left..right] is sum(diff[left+1..right])
        
        # We'll use a sliding window with left and right pointers.
        # current_sum will maintain the sum of diff from left+1 to right.
        
        left = 0
        current_sum = 0
        count = 0
        
        for right in range(n):
            # Add the cost for the transition from right-1 to right
            if right > 0:
                diff_val = max(0, nums[right-1] - nums[right])
                current_sum += diff_val
            
            # Shrink the window from the left if the cost exceeds k
            # The current_sum represents sum(diff[left+1..right])
            # When we move left to left+1, we remove diff[left+1] from the sum
            while current_sum > k and left < right:
                # Remove diff[left+1]
                diff_to_remove = max(0, nums[left] - nums[left+1])
                current_sum -= diff_to_remove
                left += 1
            
            # All subarrays ending at 'right' and starting from 'left' to 'right' are valid
            count += (right - left + 1)
            
        return count