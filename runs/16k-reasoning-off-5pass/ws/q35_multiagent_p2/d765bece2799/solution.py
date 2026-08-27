class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        
        # Helper to calculate sum of max for all subarrays of length <= k
        def sum_of_max():
            # For each element, find the left boundary: index of first element to the left that is strictly greater
            # If no such element within k distance, then left boundary is i - k
            # Right boundary: index of first element to the right that is >= (non-strict) to avoid double counting
            # If no such element within k distance, then right boundary is i + k
            
            left = [0] * n
            right = [0] * n
            
            # Monotonic decreasing stack for left boundaries (strictly greater)
            stack = []
            for i in range(n):
                # We want the nearest index to the left with value > nums[i]
                # But also constrained by i - k
                # Pop elements that are <= nums[i] because they are not greater
                while stack and nums[stack[-1]] <= nums[i]:
                    stack.pop()
                if stack:
                    left[i] = stack[-1]
                else:
                    left[i] = i - k  # no greater element found, so constrained by k
                    # But if i - k < 0, then left[i] = -1? Actually, the boundary is the index before the start of valid subarrays
                    # The number of choices for left endpoint is i - left[i]
                    # If no greater element to the left, then the leftmost valid start is max(0, i - k + 1)
                    # So the boundary index (exclusive) is max(-1, i - k)
                    if left[i] < 0:
                        left[i] = -1
                stack.append(i)
            
            # Monotonic decreasing stack for right boundaries (non-strictly greater, i.e., >=)
            stack = []
            for i in range(n - 1, -1, -1):
                # We want the nearest index to the right with value >= nums[i]
                # But also constrained by i + k
                while stack and nums[stack[-1]] < nums[i]:
                    stack.pop()
                if stack:
                    right[i] = stack[-1]
                else:
                    right[i] = i + k
                    if right[i] >= n:
                        right[i] = n
                stack.append(i)
            
            total = 0
            for i in range(n):
                # Number of subarrays where nums[i] is the maximum
                # Left choices: from left[i]+1 to i -> (i - left[i]) choices
                # Right choices: from i to right[i]-1 -> (right[i] - i) choices
                count = (i - left[i]) * (right[i] - i)
                total += nums[i] * count
            return total
        
        # Helper to calculate sum of min for all subarrays of length <= k
        def sum_of_min():
            # For each element, find the left boundary: index of first element to the left that is strictly smaller
            # Right boundary: index of first element to the right that is <= (non-strict) to avoid double counting
            
            left = [0] * n
            right = [0] * n
            
            # Monotonic increasing stack for left boundaries (strictly smaller)
            stack = []
            for i in range(n):
                # We want the nearest index to the left with value < nums[i]
                while stack and nums[stack[-1]] >= nums[i]:
                    stack.pop()
                if stack:
                    left[i] = stack[-1]
                else:
                    left[i] = i - k
                    if left[i] < 0:
                        left[i] = -1
                stack.append(i)
            
            # Monotonic increasing stack for right boundaries (non-strictly smaller, i.e., <=)
            stack = []
            for i in range(n - 1, -1, -1):
                # We want the nearest index to the right with value <= nums[i]
                while stack and nums[stack[-1]] > nums[i]:
                    stack.pop()
                if stack:
                    right[i] = stack[-1]
                else:
                    right[i] = i + k
                    if right[i] >= n:
                        right[i] = n
                stack.append(i)
            
            total = 0
            for i in range(n):
                count = (i - left[i]) * (right[i] - i)
                total += nums[i] * count
            return total
        
        return sum_of_max() + sum_of_min()