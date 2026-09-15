from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        S = sum(nums)
        # Any alternating sum lies in [-S, S]
        if k < -S or k > S:
            return -1

        offset = S
        width = 2 * S + 1
        MASK = (1 << width) - 1
        target = 1 << (k + offset)

        # ---------- Part 1: all-positive subsequences, exact product p in [1, limit] ----------
        # dp0[p] / dp1[p] : bitset of reachable alternating sums, bit = alt + offset,
        # for NON-EMPTY subsequences using only positive elements with product exactly p.
        dp0 = [0] * (limit + 1)
        dp1 = [0] * (limit + 1)

        for v in nums:
            if v == 0:
                continue
            n0 = dp0[:]          # skip transitions
            n1 = dp1[:]
            maxp = limit // v
            for p in range(1, maxp + 1):
                b = dp0[p]
                if b:            # include v while currently at even position -> +v, parity flips to 1
                    n1[p * v] |= (b << v) & MASK
                b = dp1[p]
                if b:            # include v while currently at odd position -> -v, parity flips to 0
                    n0[p * v] |= (b >> v)
            if v <= limit:       # singleton [v]
                n1[v] |= (1 << (v + offset))
            dp0 = n0
            dp1 = n1

        for p in range(limit, 0, -1):
            if (dp0[p] & target) or (dp1[p] & target):
                return p

        # ---------- Part 2: existence of a non-empty subsequence containing a zero ----------
        # dpZ[parity][hasZero] : bitsets over alternating sums, no product bound.
        # (Zeros kill the product, so we must NOT cap these states by the limit.)
        dpZ = [[0, 0], [0, 0]]
        for v in nums:
            ndpZ = [dpZ[0][:], dpZ[1][:]]
            for parity in (0, 1):
                for hz in (0, 1):
                    b = dpZ[parity][hz]
                    if not b:
                        continue
                    npar = 1 - parity
                    nhz = 1 if v == 0 else hz
                    if parity == 0:
                        sb = (b << v) & MASK
                    else:
                        sb = b >> v
                    ndpZ[npar][nhz] |= sb
            nhz = 1 if v == 0 else 0
            ndpZ[1][nhz] |= (1 << (v + offset))
            dpZ = ndpZ

        if (dpZ[0][1] & target) or (dpZ[1][1] & target):
            return 0
        return -1