from typing import List
from collections import deque
import random


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        if not nums:
            return 0

        n = len(nums)
        if k <= 0:
            return 0
        if k > n:
            k = n

        def sum_minima() -> int:
            dq = deque()
            running = 0
            total = 0

            for r, x in enumerate(nums):
                cnt = 1

                while dq and dq[-1][0] >= x:
                    v, c = dq.pop()
                    running -= v * c
                    cnt += c

                dq.append((x, cnt))
                running += x * cnt

                if r >= k:
                    v, c = dq[0]
                    running -= v
                    if c == 1:
                        dq.popleft()
                    else:
                        dq[0] = (v, c - 1)

                total += running

            return total

        def sum_maxima() -> int:
            dq = deque()
            running = 0
            total = 0

            for r, x in enumerate(nums):
                cnt = 1

                while dq and dq[-1][0] <= x:
                    v, c = dq.pop()
                    running -= v * c
                    cnt += c

                dq.append((x, cnt))
                running += x * cnt

                if r >= k:
                    v, c = dq[0]
                    running -= v
                    if c == 1:
                        dq.popleft()
                    else:
                        dq[0] = (v, c - 1)

                total += running

            return total

        return sum_minima() + sum_maxima()


def brute_force(nums: List[int], k: int) -> int:
    total = 0
    n = len(nums)

    for i in range(n):
        mn = 10**30
        mx = -10**30
        end = min(n, i + k)

        for j in range(i, end):
            v = nums[j]
            if v < mn:
                mn = v
            if v > mx:
                mx = v
            total += mn + mx

    return total


def run_tests() -> None:
    sol = Solution()

    # Given examples.
    assert sol.minMaxSubarraySum([1, 2, 3], 2) == 20
    assert sol.minMaxSubarraySum([1, -3, 1], 2) == -6

    # k = 1.
    for nums in [[7], [-1, 2, -3], [1, 1, 1], [3, -2, 0, 5]]:
        assert sol.minMaxSubarraySum(nums, 1) == brute_force(nums, 1)

    # k = n.
    for nums in [[7], [-1, 2, -3], [1, 1, 1], [3, -2, 0, 5], [5, 4, 3, 2, 1]]:
        assert sol.minMaxSubarraySum(nums, len(nums)) == brute_force(nums, len(nums))

    # All equal values.
    for n in range(1, 8):
        for x in (-2, 0, 3):
            nums = [x] * n
            for k in range(1, n + 1):
                assert sol.minMaxSubarraySum(nums, k) == brute_force(nums, k)

    # Negative values.
    for nums in [[-1, -2, -3], [-5, 0, -5], [-10**6, 10**6, -10**6]]:
        for k in range(1, len(nums) + 1):
            assert sol.minMaxSubarraySum(nums, k) == brute_force(nums, k)

    # Random small arrays.
    random.seed(2024)
    for _ in range(3000):
        n = random.randint(1, 12)
        nums = [random.randint(-6, 6) for _ in range(n)]
        k = random.randint(1, n)
        assert sol.minMaxSubarraySum(nums, k) == brute_force(nums, k)

    # Random medium arrays.
    for _ in range(100):
        n = random.randint(1, 80)
        nums = [random.randint(-10, 10) for _ in range(n)]
        k = random.randint(1, n)
        assert sol.minMaxSubarraySum(nums, k) == brute_force(nums, k)


if __name__ == "__main__":
    run_tests()