from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        def count_contributions(greater: bool) -> int:
            # prev[i] = distance to previous element that is strictly greater (if greater)
            # or strictly smaller (if not greater). If none, distance = i+1.
            prev = [0] * n
            stack = []
            for i in range(n):
                while stack:
                    top = stack[-1]
                    if greater:
                        if nums[top] <= nums[i]:
                            stack.pop()
                        else:
                            break
                    else:
                        if nums[top] >= nums[i]:
                            stack.pop()
                        else:
                            break
                if stack:
                    prev[i] = i - stack[-1]
                else:
                    prev[i] = i + 1
                stack.append(i)

            nxt = [0] * n
            stack = []
            for i in range(n - 1, -1, -1):
                while stack:
                    top = stack[-1]
                    if greater:
                        if nums[top] < nums[i]:
                            stack.pop()
                        else:
                            break
                    else:
                        if nums[top] > nums[i]:
                            stack.pop()
                        else:
                            break
                if stack:
                    nxt[i] = stack[-1] - i
                else:
                    nxt[i] = n - i
                stack.append(i)

            total = 0
            for i in range(n):
                left_min = i - prev[i] + 1
                left_max = i
                right_min = i
                right_max = i + nxt[i] - 1

                s_low = max(left_min, i - k + 1)
                s_high = i

                if s_low > s_high:
                    continue

                threshold = right_max - k + 1

                # Part 2: s in [s_low, min(s_high, threshold)] where count = s + k - i
                p2_end = min(s_high, threshold)
                if s_low <= p2_end:
                    cnt = p2_end - s_low + 1
                    sum_s = (s_low + p2_end) * cnt // 2
                    total += nums[i] * (cnt * (k - i) + sum_s)

                # Part 3: s in [max(s_low, threshold + 1), s_high] where count = right_max - i + 1
                p3_start = max(s_low, threshold + 1)
                if p3_start <= s_high:
                    cnt = s_high - p3_start + 1
                    total += nums[i] * (cnt * (right_max - i + 1))

            return total

        max_sum = count_contributions(greater=True)
        min_sum = count_contributions(greater=False)
        return max_sum + min_sum


# Verification
def brute(nums, k):
    n = len(nums)
    total = 0
    for L in range(1, min(k, n) + 1):
        for i in range(n - L + 1):
            sub = nums[i:i+L]
            total += min(sub) + max(sub)
    return total

def test():
    sol = Solution()
    assert sol.minMaxSubarraySum([1,2,3], 2) == 20, f"Example 1 failed: got {sol.minMaxSubarraySum([1,2,3], 2)}"
    assert sol.minMaxSubarraySum([1,-3,1], 2) == -6, f"Example 2 failed: got {sol.minMaxSubarraySum([1,-3,1], 2)}"
    
    import random
    random.seed(42)
    for _ in range(2000):
        n = random.randint(1, 12)
        k = random.randint(1, n)
        nums = [random.randint(-10, 10) for _ in range(n)]
        expected = brute(nums, k)
        actual = sol.minMaxSubarraySum(nums, k)
        if expected != actual:
            print(f"MISMATCH: nums={nums}, k={k}, expected={expected}, actual={actual}")
            return False
    print("All tests passed!")
    return True

test()