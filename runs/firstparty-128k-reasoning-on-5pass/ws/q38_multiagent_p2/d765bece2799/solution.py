from typing import List
from collections import deque


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def extrema_sum(is_max: bool) -> int:
            runs = deque()
            active = 0
            current = 0
            total = 0

            if is_max:
                for x in nums:
                    count = 1

                    while runs and runs[-1][0] <= x:
                        v, c = runs.pop()
                        current -= v * c
                        count += c

                    runs.append([x, count])
                    current += x * count
                    active += 1

                    if active > k:
                        v, c = runs[0]
                        current -= v
                        if c == 1:
                            runs.popleft()
                        else:
                            runs[0][1] = c - 1
                        active -= 1

                    total += current
            else:
                for x in nums:
                    count = 1

                    while runs and runs[-1][0] >= x:
                        v, c = runs.pop()
                        current -= v * c
                        count += c

                    runs.append([x, count])
                    current += x * count
                    active += 1

                    if active > k:
                        v, c = runs[0]
                        current -= v
                        if c == 1:
                            runs.popleft()
                        else:
                            runs[0][1] = c - 1
                        active -= 1

                    total += current

            return total

        return extrema_sum(True) + extrema_sum(False)


def _brute_force(nums: List[int], k: int) -> int:
    total = 0
    n = len(nums)

    for i in range(n):
        mn = mx = nums[i]
        limit = min(n, i + k)

        for j in range(i, limit):
            if j > i:
                v = nums[j]
                if v < mn:
                    mn = v
                if v > mx:
                    mx = v
            total += mn + mx

    return total


def _run_self_tests() -> None:
    import random
    import time

    sol = Solution()

    assert sol.minMaxSubarraySum([1, 2, 3], 2) == 20
    assert sol.minMaxSubarraySum([1, -3, 1], 2) == -6

    assert sol.minMaxSubarraySum([5, -2, 0, 7], 1) == 2 * (5 - 2 + 0 + 7)
    assert sol.minMaxSubarraySum([4, 1, 3, 2], 4) == _brute_force([4, 1, 3, 2], 4)
    assert sol.minMaxSubarraySum([2, 2, 2, 2], 2) == _brute_force([2, 2, 2, 2], 2)
    assert sol.minMaxSubarraySum([0, 0, -1, 0], 3) == _brute_force([0, 0, -1, 0], 3)
    assert sol.minMaxSubarraySum([-5, -1, -3], 2) == _brute_force([-5, -1, -3], 2)

    rng = random.Random(12345)
    for _ in range(3000):
        n = rng.randint(1, 9)
        nums = [rng.randint(-6, 6) for _ in range(n)]
        k = rng.randint(1, n)
        expected = _brute_force(nums, k)
        actual = sol.minMaxSubarraySum(nums, k)
        if actual != expected:
            raise AssertionError(
                f"mismatch nums={nums} k={k} expected={expected} actual={actual}"
            )

    n = 80000
    large = [rng.randint(-10**6, 10**6) for _ in range(n)]
    k = rng.randint(1, n)

    t0 = time.perf_counter()
    ans = sol.minMaxSubarraySum(large, k)
    t1 = time.perf_counter()
    print(f"large random n={n} k={k} answer={ans} time={t1 - t0:.3f}s")

    t0 = time.perf_counter()
    ans = sol.minMaxSubarraySum(large, 1)
    t1 = time.perf_counter()
    assert ans == 2 * sum(large)
    print(f"large k=1 n={n} answer={ans} time={t1 - t0:.3f}s")

    half = n // 2
    t0 = time.perf_counter()
    ans = sol.minMaxSubarraySum([10**6] * n, half)
    t1 = time.perf_counter()
    expected = 2 * (10**6) * (n * half - half * (half - 1) // 2)
    assert ans == expected
    print(f"large equal n={n} k={half} answer={ans} time={t1 - t0:.3f}s")

    t0 = time.perf_counter()
    ans = sol.minMaxSubarraySum(list(range(n)), half)
    t1 = time.perf_counter()
    print(f"large increasing n={n} k={half} answer={ans} time={t1 - t0:.3f}s")

    t0 = time.perf_counter()
    ans = sol.minMaxSubarraySum(list(range(n - 1, -1, -1)), half)
    t1 = time.perf_counter()
    print(f"large decreasing n={n} k={half} answer={ans} time={t1 - t0:.3f}s")

    print("self tests passed")


if __name__ == "__main__":
    _run_self_tests()