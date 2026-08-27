from typing import List
from collections import deque
import random


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        if not nums:
            return 0

        min_dq = deque()  # groups (minimum value, number of starts)
        max_dq = deque()  # groups (maximum value, number of starts)

        min_total = 0
        max_total = 0
        min_sum = 0
        max_sum = 0

        for r, x in enumerate(nums):
            # Update minima for all subarrays ending at r.
            cnt = 1
            while min_dq and min_dq[-1][0] >= x:
                v, c = min_dq.pop()
                cnt += c
                min_total -= v * c
            min_dq.append((x, cnt))
            min_total += x * cnt

            # Drop the oldest start if the window length would exceed k.
            if r >= k:
                v, c = min_dq[0]
                min_total -= v
                if c == 1:
                    min_dq.popleft()
                else:
                    min_dq.popleft()
                    min_dq.appendleft((v, c - 1))

            # Update maxima for all subarrays ending at r.
            cnt = 1
            while max_dq and max_dq[-1][0] <= x:
                v, c = max_dq.pop()
                cnt += c
                max_total -= v * c
            max_dq.append((x, cnt))
            max_total += x * cnt

            # Drop the oldest start if the window length would exceed k.
            if r >= k:
                v, c = max_dq[0]
                max_total -= v
                if c == 1:
                    max_dq.popleft()
                else:
                    max_dq.popleft()
                    max_dq.appendleft((v, c - 1))

            min_sum += min_total
            max_sum += max_total

        return min_sum + max_sum


def brute_force(nums: List[int], k: int) -> int:
    n = len(nums)
    total = 0
    for i in range(n):
        mn = mx = nums[i]
        total += mn + mx
        limit = min(n, i + k)
        for j in range(i + 1, limit):
            x = nums[j]
            if x < mn:
                mn = x
            if x > mx:
                mx = x
            total += mn + mx
    return total


def _run_tests() -> None:
    sol = Solution()

    # Given examples.
    assert sol.minMaxSubarraySum([1, 2, 3], 2) == 20
    assert sol.minMaxSubarraySum([1, -3, 1], 2) == -6

    # Fixed edge cases: single element, duplicates, negatives, monotone arrays.
    test_arrays = [
        [5],
        [1, 1, 1],
        [-1, -1, -1],
        [2, 2, 1, 2, 2],
        [3, 1, 2, 1, 3],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [-3, 2, -1, 4, 0],
    ]

    for nums in test_arrays:
        for k in range(1, len(nums) + 1):
            expected = brute_force(nums, k)
            got = sol.minMaxSubarraySum(nums, k)
            assert got == expected, (nums, k, got, expected)

    # Small random arrays with a fixed seed.
    random.seed(12345)
    for _ in range(300):
        n = random.randint(1, 9)
        nums = [random.randint(-6, 6) for _ in range(n)]
        k = random.randint(1, n)
        expected = brute_force(nums, k)
        got = sol.minMaxSubarraySum(nums, k)
        assert got == expected, (nums, k, got, expected)

    # Targeted random edge cases: k = 1, k = n, duplicate-heavy values.
    for _ in range(100):
        n = random.randint(1, 12)
        nums = [random.choice([0, 0, 1, -1, 2, -2]) for _ in range(n)]
        k = random.choice([1, n, random.randint(1, n)])
        expected = brute_force(nums, k)
        got = sol.minMaxSubarraySum(nums, k)
        assert got == expected, (nums, k, got, expected)

    print("All tests passed")


if __name__ == "__main__":
    _run_tests()