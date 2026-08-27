from typing import List
from itertools import combinations
import random

MOD = 1_000_000_007


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 5:
            return 0

        # Coordinate-compress values.
        comp = {}
        ids = []
        for v in nums:
            if v not in comp:
                comp[v] = len(comp)
            ids.append(comp[v])

        m = len(comp)
        left = [0] * m
        right = [0] * m
        for idx in ids:
            right[idx] += 1

        def c2(a: int) -> int:
            return a * (a - 1) // 2

        ans = 0
        range_m = range(m)

        for k in range(n):
            x = ids[k]
            right[x] -= 1  # k is the middle index, not part of either side.

            if 2 <= k <= n - 3:
                cx_l = left[x]
                cx_r = right[x]
                ln = k - cx_l
                rn = (n - 1 - k) - cx_r

                # Cases where the middle value appears at least 3 times total.
                total = c2(k) * c2(n - 1 - k)
                no_extra = c2(ln) * c2(rn)
                one_extra = cx_l * ln * c2(rn) + c2(ln) * cx_r * rn
                t_ge3 = total - no_extra - one_extra

                # Aggregates over non-x values for the exactly-two-x case.
                sum_l2 = 0
                sum_r2 = 0
                cross1 = 0  # sum l * r
                cross2 = 0  # sum l * r * r
                cross3 = 0  # sum l * l * r

                L = left
                R = right
                for v in range_m:
                    if v == x:
                        continue
                    l = L[v]
                    r = R[v]
                    sum_l2 += l * l
                    sum_r2 += r * r
                    lr = l * r
                    cross1 += lr
                    cross2 += lr * r
                    cross3 += lr * l

                # Number of unordered index pairs with distinct values on each side.
                p_l = (ln * ln - sum_l2) // 2
                p_r = (rn * rn - sum_r2) // 2

                # Cases where the middle value appears exactly 2 times total.
                t2 = (
                    cx_l * (p_r * ln - rn * cross1 + cross2)
                    + cx_r * (p_l * rn - ln * cross1 + cross3)
                )

                ans = (ans + t_ge3 + t2) % MOD

            left[x] += 1

        return ans


def brute(nums: List[int]) -> int:
    """Brute-force checker for small arrays."""
    n = len(nums)
    ans = 0
    for idxs in combinations(range(n), 5):
        seq = [nums[i] for i in idxs]
        mid = seq[2]

        freq = {}
        for val in seq:
            freq[val] = freq.get(val, 0) + 1

        maxc = max(freq.values())
        if freq[mid] == maxc and sum(1 for c in freq.values() if c == maxc) == 1:
            ans += 1

    return ans


def _run_tests() -> None:
    sol = Solution()

    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]

    for nums, expected in examples:
        got = sol.subsequencesWithMiddleMode(nums)
        assert got == expected, (nums, got, expected)
        assert brute(nums) == expected, (nums, brute(nums), expected)

    # All-same arrays: every 5-subsequence is valid.
    for n in range(5, 11):
        nums = [7] * n
        expected = (n * (n - 1) * (n - 2) * (n - 3) * (n - 4)) // 120
        got = sol.subsequencesWithMiddleMode(nums)
        assert got == expected % MOD, (nums, got, expected)
        assert brute(nums) == expected, (nums, brute(nums), expected)

    # All-distinct array: no valid subsequence.
    nums = list(range(9))
    got = sol.subsequencesWithMiddleMode(nums)
    assert got == 0, (nums, got)
    assert brute(nums) == 0, (nums, brute(nums))

    # Small hand-checked cases.
    got = sol.subsequencesWithMiddleMode([1, 2, 2, 3, 4])
    assert got == 1, (got,)
    assert brute([1, 2, 2, 3, 4]) == 1

    got = sol.subsequencesWithMiddleMode([1, 2, 2, 3, 3])
    assert got == 0, (got,)
    assert brute([1, 2, 2, 3, 3]) == 0

    random.seed(2024)

    # General random small arrays.
    for _ in range(120):
        n = random.randint(5, 8)
        pool = random.choice([
            [-1, 0, 1],
            [0, 1],
            [0, 1, 2],
            [-5, -1, 0, 1, 2],
            list(range(n)),
        ])
        nums = [random.choice(pool) for _ in range(n)]
        expected = brute(nums)
        got = sol.subsequencesWithMiddleMode(nums)
        assert got == expected, (nums, got, expected)

    # Duplicate-heavy arrays.
    for _ in range(60):
        n = random.randint(5, 9)
        nums = [random.choice([0, 1, 2]) for _ in range(n)]
        expected = brute(nums)
        got = sol.subsequencesWithMiddleMode(nums)
        assert got == expected, (nums, got, expected)

    # Negative values.
    for _ in range(60):
        n = random.randint(5, 8)
        nums = [random.choice([-100, -1, 0, 1, 100]) for _ in range(n)]
        expected = brute(nums)
        got = sol.subsequencesWithMiddleMode(nums)
        assert got == expected, (nums, got, expected)


if __name__ == "__main__":
    _run_tests()