from typing import List
from collections import Counter
from itertools import combinations

MOD = 10**9 + 7


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)

        def c2(x: int) -> int:
            return x * (x - 1) // 2 if x >= 2 else 0

        left = Counter()
        right = Counter(nums)
        ss_left = 0                      # sum of squared frequencies on left
        ss_right = sum(c * c for c in right.values())

        l = 0
        r = n
        ans = 0

        for i, v in enumerate(nums):
            # Move nums[i] out of the right side; i is the fixed middle index.
            old = right[v]
            right[v] = old - 1
            ss_right += (old - 1) * (old - 1) - old * old
            if right[v] == 0:
                del right[v]
            r -= 1

            lv = left.get(v, 0)
            rv = right.get(v, 0)

            if l >= 2 and r >= 2:
                # Left/right pair counts classified by how many chosen elements equal v.
                L0 = c2(l - lv)
                L1 = lv * (l - lv)
                L2 = c2(lv)
                R0 = c2(r - rv)
                R1 = rv * (r - rv)
                R2 = c2(rv)
                Rtot = c2(r)

                # If at least two side elements equal v, the middle value is always unique.
                ans += L2 * Rtot + L1 * (R1 + R2) + L0 * R2

                # Exactly one side element equals v: the three non-v side values must be distinct.
                # Left has (v, a), right has two distinct non-v values different from a.
                mR = r - rv
                if lv and mR >= 2:
                    SR = ss_right - rv * rv
                    DR = (mR * mR - SR) // 2  # distinct-valued non-v pairs on right
                    add = 0
                    for a, ca in left.items():
                        if a == v:
                            continue
                        ra = right.get(a, 0)
                        add += ca * (DR - ra * (mR - ra))
                    ans += lv * add

                # Right has (v, a), left has two distinct non-v values different from a.
                mL = l - lv
                if rv and mL >= 2:
                    SL = ss_left - lv * lv
                    DL = (mL * mL - SL) // 2  # distinct-valued non-v pairs on left
                    add = 0
                    for a, ca in right.items():
                        if a == v:
                            continue
                        la = left.get(a, 0)
                        add += ca * (DL - la * (mL - la))
                    ans += rv * add

            # Move nums[i] into the left side for the next middle index.
            old = left.get(v, 0)
            left[v] = old + 1
            ss_left += (old + 1) * (old + 1) - old * old
            l += 1

        return ans % MOD


def brute_force(nums: List[int]) -> int:
    n = len(nums)
    ans = 0
    for idxs in combinations(range(n), 5):
        seq = [nums[i] for i in idxs]
        mid = seq[2]
        cnt = Counter(seq)
        mx = max(cnt.values())
        if cnt[mid] == mx and sum(1 for x in cnt.values() if x == mx) == 1:
            ans += 1
    return ans % MOD


if __name__ == "__main__":
    import random

    examples = [
        ([1, 1, 1, 1, 1, 1], 6),
        ([1, 2, 2, 3, 3, 4], 4),
        ([0, 1, 2, 3, 4, 5, 6, 7, 8], 0),
    ]
    sol = Solution()
    for arr, want in examples:
        got = sol.subsequencesWithMiddleMode(arr)
        assert got == want, (arr, got, want)
        assert brute_force(arr) == want, (arr, brute_force(arr), want)

    random.seed(0)
    for n in range(5, 11):
        for _ in range(300):
            arr = [random.randint(0, 4) for _ in range(n)]
            got = sol.subsequencesWithMiddleMode(arr)
            want = brute_force(arr)
            assert got == want, (arr, got, want)
    print("all tests passed")