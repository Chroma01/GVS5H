from typing import List
from collections import deque
import random
import sys


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        min_dq = deque()
        max_dq = deque()
        min_sum = 0
        max_sum = 0
        ans = 0

        for i, x in enumerate(nums):
            # Add x as the new right endpoint.
            # For minima, previous groups with value > x become x.
            cnt = 1
            while min_dq and min_dq[-1][0] > x:
                v, c = min_dq.pop()
                min_sum -= v * c
                cnt += c

            if min_dq and min_dq[-1][0] == x:
                min_dq[-1][1] += cnt
            else:
                min_dq.append([x, cnt])
            min_sum += x * cnt

            # For maxima, previous groups with value < x become x.
            cnt = 1
            while max_dq and max_dq[-1][0] < x:
                v, c = max_dq.pop()
                max_sum -= v * c
                cnt += c

            if max_dq and max_dq[-1][0] == x:
                max_dq[-1][1] += cnt
            else:
                max_dq.append([x, cnt])
            max_sum += x * cnt

            # If the temporary window has k + 1 left endpoints,
            # remove the oldest one from the front group.
            if i >= k:
                v, c = min_dq[0]
                min_sum -= v
                if c == 1:
                    min_dq.popleft()
                else:
                    min_dq[0][1] = c - 1

                v, c = max_dq[0]
                max_sum -= v
                if c == 1:
                    max_dq.popleft()
                else:
                    max_dq[0][1] = c - 1

            ans += min_sum + max_sum

        return ans


def brute_force(nums: List[int], k: int) -> int:
    total = 0
    n = len(nums)
    for i in range(n):
        mn = nums[i]
        mx = nums[i]
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


def run_verification() -> int:
    sol = Solution()
    failures = []

    def fmt(nums: List[int]) -> str:
        if len(nums) <= 20:
            return str(nums)
        head = ", ".join(map(str, nums[:5]))
        tail = ", ".join(map(str, nums[-5:]))
        return f"[{head}, ..., {tail}] len={len(nums)}"

    def check(name, nums, k, expected=None, verbose=False):
        actual = sol.minMaxSubarraySum(nums, k)
        if expected is None:
            expected = brute_force(nums, k)
        if actual != expected:
            failures.append((name, k, expected, actual))
            print(f"FAIL {name}: k={k} expected={expected} actual={actual} nums={fmt(nums)}")
        elif verbose:
            print(f"PASS {name}: k={k} result={actual} nums={fmt(nums)}")

    # Provided examples.
    check("example1", [1, 2, 3], 2, 20, True)
    check("example2", [1, -3, 1], 2, -6, True)

    # Targeted edge cases.
    check("single positive", [42], 1, 84, True)
    check("single negative", [-1], 1, -2, True)
    check("k1 increasing", [1, 2, 3], 1, 12, True)
    check("k1 mixed", [-5, 0, 7], 1, 4, True)
    check("k_n increasing", [1, 2, 3], 3, 24, True)
    check("k_n mixed", [1, -3, 1], 3, -8, True)
    check("k larger than n", [1, 2, 3], 5, 24, True)
    check("all equal k2", [5, 5, 5], 2, 50, True)
    check("all equal k3", [5, 5, 5], 3, 60, True)
    check("all zeros", [0, 0, 0, 0], 2, 0, True)
    check("negative k2", [-1, -2, -3], 2, -20, True)
    check("negative k1", [-1, -2, -3], 1, -12, True)
    check("negative k_n", [-1, -2, -3], 3, -24, True)
    check("increasing k2", [1, 2, 3, 4], 2, None, True)
    check("decreasing k2", [4, 3, 2, 1], 2, None, True)
    check("alternating k3", [1, -1, 1, -1, 1], 3, None, True)
    check("duplicates mixed", [2, 1, 2, 1, 2], 3, None, True)
    check("large values small n", [10**6, -10**6, 10**6], 2, None, True)

    # Random brute-force comparisons with a fixed seed.
    rng = random.Random(20240527)
    random_count = 0

    for _ in range(3000):
        n = rng.randint(1, 8)
        k = rng.randint(1, n)
        nums = [rng.randint(-5, 5) for _ in range(n)]
        check("random small", nums, k)
        random_count += 1

    for _ in range(500):
        n = rng.randint(1, 20)
        k = rng.randint(1, n)
        nums = [rng.randint(-100, 100) for _ in range(n)]
        check("random medium", nums, k)
        random_count += 1

    for _ in range(100):
        n = rng.randint(1, 40)
        k = rng.randint(1, n)
        nums = [rng.randint(-10**6, 10**6) for _ in range(n)]
        check("random large values", nums, k)
        random_count += 1

    print(f"Random tests: {random_count} cases checked.")

    # Large all-equal cases with closed-form expected values.
    n = 80000
    big = [1] * n

    k = n
    count = k * (n + 1) - k * (k + 1) // 2
    check("large k_n all equal", big, k, 2 * count, True)

    k = n // 2
    count = k * (n + 1) - k * (k + 1) // 2
    check("large half window all equal", big, k, 2 * count, True)

    if failures:
        print(f"Total failures: {len(failures)}")
        return 1

    print("All tests passed.")
    return 0


if __name__ == "__main__":
    sys.exit(run_verification())