from typing import List
from itertools import combinations


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0

        # Coordinate compression.
        comp = {}
        arr = []
        for v in nums:
            if v not in comp:
                comp[v] = len(comp)
            arr.append(comp[v])

        m = len(comp)
        left = [0] * m
        right = [0] * m

        # dupL/dupR store sum_v C(freq[v], 2) on each side.
        dupR = 0
        for v in arr:
            dupR += right[v]
            right[v] += 1
        dupL = 0

        # Precompute C(i, 2).
        c2 = [0] * (n + 1)
        for i in range(2, n + 1):
            c2[i] = i * (i - 1) // 2

        ans = 0
        values = range(m)

        for mid in range(n):
            x = arr[mid]

            # Move current index out of the right side.
            old = right[x]
            dupR -= old - 1
            right[x] = old - 1

            L = mid
            R = n - mid - 1

            if L >= 2 and R >= 2:
                Lx = left[x]
                Rx = right[x]
                Lnx = L - Lx
                Rnx = R - Rx

                # Left pair counts by number of x's: 0, 1, 2.
                L0 = c2[Lnx]
                L1 = Lx * Lnx
                L2 = c2[Lx]

                # Right pair counts by number of x's: 0, 1, 2.
                R0 = c2[Rnx]
                R1 = Rx * Rnx
                R2 = c2[Rx]

                # Cases where the middle value appears at least twice among sides.
                valid = L2 * (R0 + R1 + R2) + L1 * (R1 + R2) + L0 * R2

                # Cases where exactly one side element equals x.
                if Lx or Rx:
                    # Number of non-x pairs with distinct values on each side.
                    D2L = L0 - (dupL - L2)
                    D2R = R0 - (dupR - R2)

                    sLR = 0  # left has one x, right has zero x
                    sRL = 0  # right has one x, left has zero x

                    for y in values:
                        if y == x:
                            continue

                        fl = left[y]
                        fr = right[y]

                        if fl:
                            # Right pair must have distinct values and avoid y.
                            sLR += fl * (D2R - fr * (Rnx - fr))

                        if fr:
                            # Left pair must have distinct values and avoid y.
                            sRL += fr * (D2L - fl * (Lnx - fl))

                    valid += Lx * sLR + Rx * sRL

                ans = (ans + valid) % MOD

            # Move current index into the left side for future middles.
            oldL = left[x]
            dupL += oldL
            left[x] = oldL + 1

        return ans


def brute_force(nums: List[int]) -> int:
    n = len(nums)
    ans = 0

    for combo in combinations(range(n), 5):
        mid_val = nums[combo[2]]
        freq = {}

        for idx in combo:
            v = nums[idx]
            freq[v] = freq.get(v, 0) + 1

        mid_count = freq[mid_val]
        max_other = 0

        for v, c in freq.items():
            if v != mid_val and c > max_other:
                max_other = c

        if mid_count > max_other:
            ans += 1

    return ans


def run_tests() -> bool:
    sol = Solution()

    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]

    for nums, expected in examples:
        got = sol.subsequencesWithMiddleMode(nums)
        assert got == expected, (nums, got, expected)
        print(f"Example {nums} -> {got}")

    deterministic = [
        [1, 2, 3, 4, 5],
        [1, 2, 1, 2, 1],
        [1, 2, 2, 2, 1],
        [1, 1, 2, 1, 1],
        [1, 1, 1, 2, 2],
        [1, 2, 1, 3, 4],
        [1, 2, 1, 3, 2],
        [1, 1, 2, 1, 2],
        [1, 2, 3, 1, 2],
        [1, 2, 3, 1, 2, 1],
    ]

    for nums in deterministic:
        got = sol.subsequencesWithMiddleMode(nums)
        expected = brute_force(nums)
        assert got == expected, (nums, got, expected)

    MOD = 10**9 + 7

    def comb_mod(n: int, k: int) -> int:
        if k < 0 or k > n:
            return 0
        k = min(k, n - k)
        res = 1
        for i in range(1, k + 1):
            res = res * (n - k + i) // i
        return res % MOD

    # Large sanity checks:
    # all equal -> every 5-subsequence is valid, answer C(n, 5)
    # all distinct -> middle value appears once, never unique mode
    for n in (5, 6, 10, 1000):
        nums = [7] * n
        assert sol.subsequencesWithMiddleMode(nums) == comb_mod(n, 5)

        nums = list(range(n))
        assert sol.subsequencesWithMiddleMode(nums) == 0

    import random

    random.seed(12345)

    for _ in range(200):
        n = random.randint(5, 10)
        value_count = random.randint(1, 4)
        nums = [random.randint(1, value_count) for _ in range(n)]

        got = sol.subsequencesWithMiddleMode(nums)
        expected = brute_force(nums)
        assert got == expected, (nums, got, expected)

    for _ in range(100):
        n = random.randint(5, 12)
        nums = [random.randint(-5, 5) for _ in range(n)]

        got = sol.subsequencesWithMiddleMode(nums)
        expected = brute_force(nums)
        assert got == expected, (nums, got, expected)

    print("All tests passed")
    return True


if __name__ == "__main__":
    run_tests()