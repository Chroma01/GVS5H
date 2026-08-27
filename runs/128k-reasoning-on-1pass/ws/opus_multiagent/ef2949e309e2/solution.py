from typing import List
from collections import Counter


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)
        if n < 5:
            return 0

        cntR = Counter(nums)
        cntL = Counter()

        # Aggregates over all values y:
        # A  = sum C(cntR[y], 2)
        # Ap = sum C(cntL[y], 2)
        # B  = sum cntL[y]*cntR[y]
        # C3 = sum cntL[y]*cntR[y]^2
        # D3 = sum cntR[y]*cntL[y]^2
        A = 0
        for r in cntR.values():
            A += r * (r - 1) // 2
        Ap = 0
        B = 0
        C3 = 0
        D3 = 0

        total = 0

        for i in range(n):
            x = nums[i]

            # ---- remove index i from the right multiset ----
            r = cntR[x]
            l = cntL[x]
            A -= (r - 1)
            B -= l
            C3 -= l * (2 * r - 1)
            D3 -= l * l
            cntR[x] = r - 1

            L = i
            R = n - 1 - i
            if L >= 2 and R >= 2:
                a = cntL[x]          # copies of x strictly left of i
                b = cntR[x]          # copies of x strictly right of i
                Lp = L - a           # non-x elements on the left
                Rp = R - b           # non-x elements on the right

                Bx = B - a * b       # sum over y != x of cntL[y]*cntR[y]

                # x taken once more from the left: 1 left non-x + 2 right non-x contain a repeat
                leftsum = Lp * (A - b * (b - 1) // 2) + (Rp * Bx - (C3 - a * b * b))
                # x taken once more from the right: 2 left non-x + 1 right non-x contain a repeat
                rightsum = Rp * (Ap - a * (a - 1) // 2) + (Lp * Bx - (D3 - b * a * a))

                bad2 = a * leftsum + b * rightsum

                tot = (L * (L - 1) // 2) * (R * (R - 1) // 2)
                bad1 = (Lp * (Lp - 1) // 2) * (Rp * (Rp - 1) // 2)

                total += tot - bad1 - bad2

            # ---- add index i to the left multiset ----
            l = cntL[x]
            r = cntR[x]
            Ap += l
            B += r
            C3 += r * r
            D3 += r * (2 * l + 1)
            cntL[x] = l + 1

        return total % MOD


if __name__ == "__main__":
    s = Solution()
    assert s.subsequencesWithMiddleMode([1, 1, 1, 1, 1, 1]) == 6
    assert s.subsequencesWithMiddleMode([1, 2, 2, 3, 3, 4]) == 4
    assert s.subsequencesWithMiddleMode([0, 1, 2, 3, 4, 5, 6, 7, 8]) == 0

    # brute force cross-check on small random arrays
    import random
    from itertools import combinations

    def brute(nums):
        n = len(nums)
        res = 0
        for comb in combinations(range(n), 5):
            vals = [nums[j] for j in comb]
            mid = vals[2]
            c = Counter(vals)
            mx = max(c.values())
            if c[mid] == mx and sum(1 for v in c.values() if v == mx) == 1:
                res += 1
        return res % (10 ** 9 + 7)

    random.seed(0)
    for _ in range(300):
        n = random.randint(5, 9)
        arr = [random.randint(0, 3) for _ in range(n)]
        e = brute(arr)
        g = s.subsequencesWithMiddleMode(arr)
        assert e == g, (arr, e, g)
    print("all tests passed")