from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        if abs(k) > total:
            return -1

        offset = total
        mask = (1 << (2 * total + 1)) - 1
        target_bit = 1 << (k + offset)

        # dp0[p]: bitset of sums for non-empty even-length subsequences with product p
        # dp1[p]: bitset of sums for non-empty odd-length subsequences with product p
        dp0 = [0] * (limit + 1)
        dp1 = [0] * (limit + 1)

        for x in nums:
            # Positive product cannot include 0, and a factor > limit is impossible.
            if x == 0 or x > limit:
                continue

            d0 = dp0
            d1 = dp1
            m = mask
            xx = x

            # Descending product order prevents reusing the current element.
            # For x == 1, target product is the same index, so old snapshots are essential.
            for p in range(limit // xx, 0, -1):
                old0 = d0[p]
                old1 = d1[p]

                if old0 or old1:
                    q = p * xx

                    if old0:
                        # Append x to an even-length subsequence: next sign is +.
                        d1[q] |= (old0 << xx) & m

                    if old1:
                        # Append x to an odd-length subsequence: next sign is -.
                        d0[q] |= old1 >> xx

            # Singleton subsequence [x], odd length, product x, alternating sum +x.
            dp1[x] |= 1 << (offset + x)

        # Any positive product is better than product 0.
        for p in range(limit, 0, -1):
            if (dp0[p] | dp1[p]) & target_bit:
                return p

        # Feasibility DP for subsequences containing at least one zero.
        # no0/no1: no zero included, even/odd length. no0 includes the empty subsequence.
        # has0/has1: at least one zero included, even/odd length.
        no0 = 1 << offset
        no1 = 0
        has0 = 0
        has1 = 0

        for x in nums:
            old_no0, old_no1, old_has0, old_has1 = no0, no1, has0, has1

            if x == 0:
                # Taking zero toggles parity, leaves sum unchanged, and makes product zero.
                has0 = old_has0 | old_has1 | old_no1
                has1 = old_has1 | old_has0 | old_no0
            else:
                # Taking positive x toggles parity and shifts sum by +x or -x.
                no0 = old_no0 | (old_no1 >> x)
                no1 = old_no1 | ((old_no0 << x) & mask)

                has0 = old_has0 | (old_has1 >> x)
                has1 = old_has1 | ((old_has0 << x) & mask)

        if (has0 | has1) & target_bit:
            return 0

        return -1