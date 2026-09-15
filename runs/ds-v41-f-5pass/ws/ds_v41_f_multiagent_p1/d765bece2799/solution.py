from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        size = len(nums)
        cap = k - 1  # maximum allowed value of (u + v), where u,v are extensions

        def tri(t):
            # number of nonnegative integer pairs (u, v) with u + v <= t
            if t < 0:
                return 0
            return (t + 1) * (t + 2) // 2

        def pairs(a, b):
            # a = # valid left-endpoint choices, b = # valid right-endpoint choices.
            # Count pairs of extensions (u, v), 0<=u<a, 0<=v<b, with u+v <= cap.
            A = a - 1
            B = b - 1
            return (tri(cap) - tri(cap - A - 1)
                    - tri(cap - B - 1) + tri(cap - A - B - 2))

        # ---- minimum pass: attribute each subarray to its rightmost minimum ----
        prev_less = [-1] * size          # nearest j < i with nums[j] < nums[i]
        stack = []
        for i in range(size):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            prev_less[i] = stack[-1] if stack else -1
            stack.append(i)

        next_le = [size] * size          # nearest j > i with nums[j] <= nums[i]
        stack = []
        for i in range(size - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            next_le[i] = stack[-1] if stack else size
            stack.append(i)

        total = 0
        for i in range(size):
            total += nums[i] * pairs(i - prev_less[i], next_le[i] - i)

        # ---- maximum pass: attribute each subarray to its rightmost maximum ----
        prev_greater = [-1] * size       # nearest j < i with nums[j] > nums[i]
        stack = []
        for i in range(size):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            prev_greater[i] = stack[-1] if stack else -1
            stack.append(i)

        next_ge = [size] * size          # nearest j > i with nums[j] >= nums[i]
        stack = []
        for i in range(size - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            next_ge[i] = stack[-1] if stack else size
            stack.append(i)

        for i in range(size):
            total += nums[i] * pairs(i - prev_greater[i], next_ge[i] - i)

        return total


if __name__ == "__main__":
    import random

    def brute(nums, k):
        s = 0
        n = len(nums)
        for i in range(n):
            for j in range(i, min(n, i + k)):
                sub = nums[i:j + 1]
                s += min(sub) + max(sub)
        return s

    sol = Solution()
    assert sol.minMaxSubarraySum([1, 2, 3], 2) == 20
    assert sol.minMaxSubarraySum([1, -3, 1], 2) == -6
    random.seed(0)
    for _ in range(2000):
        n = random.randint(1, 9)
        a = [random.randint(-4, 4) for _ in range(n)]
        k = random.randint(1, n)
        assert sol.minMaxSubarraySum(a, k) == brute(a, k), (a, k)
    print("stress OK")