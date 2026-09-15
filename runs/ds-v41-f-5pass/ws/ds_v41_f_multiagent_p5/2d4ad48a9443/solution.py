from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        # Reverse: making nums[l..r] non-decreasing by increments is equivalent to
        # making the mirrored subarray of b = nums[::-1] non-increasing, same cost.
        b = nums[::-1]
        n = len(b)

        # Monotonic deque of suffix-max groups (value, count), values strictly
        # decreasing left->right. Stored in flat arrays with head/tail indices.
        vals = [0] * (n + 2)
        cnts = [0] * (n + 2)
        head = 0
        tail = 0

        total_sufmax = 0   # sum of suffix maxima over current window [left..j]
        total_sum = 0      # sum of b over current window [left..j]

        ans = 0
        left = 0
        for j in range(n):
            x = b[j]
            # Append x: every position whose suffix max <= x becomes x.
            # These are exactly the rightmost groups with value <= x.
            cnt = 1
            while tail > head and vals[tail - 1] <= x:
                tail -= 1
                total_sufmax -= vals[tail] * cnts[tail]
                cnt += cnts[tail]
            vals[tail] = x
            cnts[tail] = cnt
            tail += 1
            total_sufmax += x * cnt
            total_sum += x

            # Shrink from the left while the window cost exceeds k.
            # Removing the leftmost position never changes other suffix maxima.
            while total_sufmax - total_sum > k:
                total_sufmax -= vals[head]
                total_sum -= b[left]
                if cnts[head] == 1:
                    head += 1
                else:
                    cnts[head] -= 1
                left += 1

            ans += j - left + 1

        return ans