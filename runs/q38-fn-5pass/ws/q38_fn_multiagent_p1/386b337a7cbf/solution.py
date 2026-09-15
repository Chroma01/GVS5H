from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        max_sum = sum(nums)
        if k < -max_sum or k > max_sum:
            return -1

        offset = max_sum
        mask = (1 << (2 * max_sum + 1)) - 1

        lim = limit
        over = lim + 1
        size = over + 1

        # dp0[p]: bitset of sums for non-empty subsequences with product category p
        #         and next sign is + (current length even).
        # dp1[p]: same, but next sign is - (current length odd).
        dp0 = [0] * size
        dp1 = [0] * size

        for x in nums:
            old0 = dp0[:]
            old1 = dp1[:]

            # Start a new non-empty subsequence [x].
            if x == 0:
                start = 0
            elif x <= lim:
                start = x
            else:
                start = over
            dp1[start] |= 1 << (offset + x)

            if x == 0:
                # Appending zero: sum unchanged, parity flips, product becomes 0.
                acc0 = 0
                acc1 = 0
                for b0, b1 in zip(old0, old1):
                    acc0 |= b0
                    acc1 |= b1
                dp1[0] |= acc0
                dp0[0] |= acc1
            else:
                # Append x to all previous non-empty subsequences.
                for p in range(size):
                    b0 = old0[p]
                    b1 = old1[p]
                    if not (b0 or b1):
                        continue

                    if p == 0:
                        nxt = 0
                    elif p == over:
                        nxt = over
                    else:
                        prod = p * x
                        nxt = prod if prod <= lim else over

                    if b0:
                        dp1[nxt] |= (b0 << x) & mask
                    if b1:
                        dp0[nxt] |= b1 >> x

        target = 1 << (offset + k)
        for p in range(lim, -1, -1):
            if (dp0[p] | dp1[p]) & target:
                return p
        return -1