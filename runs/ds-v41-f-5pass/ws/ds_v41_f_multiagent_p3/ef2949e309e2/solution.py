from typing import List
from collections import Counter
import itertools
import random


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        def c2(a: int) -> int:
            return a * (a - 1) // 2 if a >= 2 else 0

        right = Counter(nums[1:])
        left = Counter()
        ans = 0

        for m in range(n):
            x = nums[m]
            L = m
            R = n - 1 - m
            lx = left[x]
            rx = right[x]
            PL = L - lx
            PR = R - rx

            CL2 = c2(L)
            CR2 = c2(R)
            CLa2 = c2(PL)
            CRb2 = c2(PR)
            a1 = lx * PL
            b1 = rx * PR

            valid = CL2 * CR2 - CLa2 * CRb2 - (a1 * CRb2 + CLa2 * b1)

            SR = 0
            U = 0
            for v, cr in right.items():
                if v == x:
                    continue
                if cr >= 2:
                    SR += cr * (cr - 1) // 2
                cl = left.get(v, 0)
                if cl:
                    U += cr * cl * (PL - cl)

            SL = 0
            T = 0
            for v, cl in left.items():
                if v == x:
                    continue
                if cl >= 2:
                    SL += cl * (cl - 1) // 2
                cr = right.get(v, 0)
                if cr:
                    T += cl * cr * (PR - cr)

            c10 = lx * (PL * (CRb2 - SR) - T)
            c01 = rx * (PR * (CLa2 - SL) - U)

            ans = (ans + valid + c10 + c01) % MOD

            left[x] += 1
            if m + 1 < n:
                nxt = nums[m + 1]
                right[nxt] -= 1
                if right[nxt] == 0:
                    del right[nxt]

        return ans % MOD


def brute(nums):
    MOD = 10**9 + 7
    n = len(nums)
    ans = 0
    for comb in itertools.combinations(range(n), 5):
        vals = [nums[i] for i in comb]
        mid = vals[2]
        cnt = Counter(vals)
        if cnt[mid] > max((cnt[v] for v in cnt if v != mid), default=0):
            ans += 1
    return ans % MOD


def main():
    sol = Solution()
    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]
    print("Examples:")
    for nums, expected in examples:
        got = sol.subsequencesWithMiddleMode(nums)
        print(f"  {nums} -> {got} (expected {expected})")
        assert got == expected, (nums, got, expected)

    random.seed(123456)
    total = 5000
    mismatches = 0
    first_fail = None
    for _ in range(total):
        n = random.randint(5, 9)
        k = random.choice([2, 3, 4])
        nums = [random.randrange(k) for _ in range(n)]
        got = sol.subsequencesWithMiddleMode(nums)
        exp = brute(nums)
        if got != exp:
            mismatches += 1
            if first_fail is None:
                first_fail = (nums, got, exp)
    print(f"Random tests: {total}, mismatches: {mismatches}")
    if first_fail:
        print("First failing input:", first_fail)
    else:
        print("First failing input: none")

    structured = [
        [0] * 5,
        [0] * 6,
        [0, 1, 2, 3, 4],
        [0, 0, 1, 1, 2],
        [0, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1],
        [0, 1, 0, 1, 0, 1, 0],
    ]
    for nums in structured:
        got = sol.subsequencesWithMiddleMode(nums)
        exp = brute(nums)
        assert got == exp, (nums, got, exp)
    print("Structured tests passed.")


if __name__ == "__main__":
    main()