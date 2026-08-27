class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        l = 0
        current_cost = 0
        count = 0
        
        for r in range(n):
            # When expanding to include nums[r], we need to consider the pair (r-1, r)
            # if r > 0. The cost is max(0, nums[r-1] - nums[r])
            if r > 0:
                if nums[r] < nums[r-1]:
                    current_cost += nums[r-1] - nums[r]
            
            # If current_cost exceeds k, shrink from the left
            while current_cost > k and l < r:
                # When removing nums[l], we remove the cost associated with the pair (l, l+1)
                # which is max(0, nums[l] - nums[l+1])
                if nums[l+1] < nums[l]:
                    current_cost -= nums[l] - nums[l+1]
                l += 1
            
            # Now the window [l, r] is valid
            count += (r - l + 1)
            
        return count