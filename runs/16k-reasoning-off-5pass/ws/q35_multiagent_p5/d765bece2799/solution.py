class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def get_contribution_sum(nums, k, is_max):
            n = len(nums)
            # left[i] will store the distance to the previous extreme element
            # right[i] will store the distance to the next extreme element
            left = [0] * n
            right = [0] * n
            
            # Monotonic stack to find left boundaries
            stack = []
            for i in range(n):
                if is_max:
                    # For max: find previous greater element
                    # Use >= to pop equal elements, so left boundary stops at strictly greater
                    # This means for duplicates, the leftmost one will have a larger left range
                    while stack and nums[stack[-1]] <= nums[i]:
                        stack.pop()
                else:
                    # For min: find previous smaller element
                    # Use <= to pop equal elements
                    while stack and nums[stack[-1]] >= nums[i]:
                        stack.pop()
                
                if stack:
                    left[i] = i - stack[-1]
                else:
                    left[i] = i + 1
                stack.append(i)
            
            # Monotonic stack to find right boundaries
            stack = []
            for i in range(n - 1, -1, -1):
                if is_max:
                    # For max: find next greater or equal element
                    # Use > to pop, so right boundary stops at greater or equal
                    # This ensures that for duplicates, the rightmost one gets the full right range
                    while stack and nums[stack[-1]] < nums[i]:
                        stack.pop()
                else:
                    # For min: find next smaller or equal element
                    # Use < to pop
                    while stack and nums[stack[-1]] > nums[i]:
                        stack.pop()
                
                if stack:
                    right[i] = stack[-1] - i
                else:
                    right[i] = n - i
                stack.append(i)
            
            total = 0
            for i in range(n):
                L = left[i]
                R = right[i]
                val = nums[i]
                
                # We need to count pairs (s, e) such that:
                # s in [i - L + 1, i]
                # e in [i, i + R - 1]
                # e - s + 1 <= k  =>  e <= s + k - 1
                
                # Let M = i + R - 1 (max possible end)
                # For a given s, valid e are in [i, min(M, s + k - 1)]
                # Count for s is max(0, min(M, s + k - 1) - i + 1)
                
                # Split s range into two parts:
                # Part 1: s + k - 1 >= M  =>  s >= M - k + 1 = i + R - k
                #   In this case, min(M, s + k - 1) = M, count = M - i + 1 = R
                # Part 2: s + k - 1 < M  =>  s < i + R - k
                #   In this case, min(M, s + k - 1) = s + k - 1, count = s + k - i
                
                # Determine the split point
                split_s = i + R - k
                
                # Part 1: s in [max(i - L + 1, split_s), i]
                start1 = max(i - L + 1, split_s)
                end1 = i
                count1 = 0
                if start1 <= end1:
                    # Number of s values
                    num_s1 = end1 - start1 + 1
                    # Each contributes R
                    count1 = num_s1 * R
                
                # Part 2: s in [i - L + 1, min(i, split_s - 1)]
                start2 = i - L + 1
                end2 = min(i, split_s - 1)
                count2 = 0
                if start2 <= end2:
                    # Sum of (s + k - i) for s from start2 to end2
                    # = sum(s) + (k - i) * num_s
                    num_s2 = end2 - start2 + 1
                    sum_s = (start2 + end2) * num_s2 // 2
                    count2 = sum_s + (k - i) * num_s2
                
                total += val * (count1 + count2)
            
            return total
        
        return get_contribution_sum(nums, k, True) + get_contribution_sum(nums, k, False)