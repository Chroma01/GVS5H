from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        OFFSET = 1800  # max |alternating sum| = 150 * 12

        # Quick impossibility: alternating sum can never exceed +/-1800.
        if k < -OFFSET or k > OFFSET:
            return -1

        OVERFLOW = limit + 1  # bucket meaning "product > limit"

        # dp[(product, parity)] -> int bitset of achievable alternating sums
        # (bit i set <=> sum = i - OFFSET achievable).
        # Only NON-EMPTY subsequences are stored; the empty subsequence is
        # used implicitly as a seed at every element.
        dp = {}

        for v in nums:
            add = {}

            # Start a new subsequence consisting of just [v]:
            # product = v (capped), sum = +v, length parity = 1.
            p0 = v if v <= limit else OVERFLOW
            key0 = (p0, 1)
            add[key0] = add.get(key0, 0) | (1 << (OFFSET + v))

            for (p, par), bits in dp.items():
                # New product, capped at OVERFLOW.
                if p == OVERFLOW:
                    p2 = 0 if v == 0 else OVERFLOW
                else:
                    prod = p * v
                    p2 = prod if prod <= limit else OVERFLOW

                # Appending v: sign is + if current length is even (par == 0),
                # - if current length is odd (par == 1).
                if par == 0:
                    bits2 = bits << v
                else:
                    bits2 = bits >> v

                key = (p2, 1 - par)
                add[key] = add.get(key, 0) | bits2

            # Merge additions into dp (OR the bitsets).
            for key, bits in add.items():
                if key in dp:
                    dp[key] |= bits
                else:
                    dp[key] = bits

        target_bit = 1 << (OFFSET + k)
        best = -1
        for (p, par), bits in dp.items():
            if p <= limit and (bits & target_bit):
                if p > best:
                    best = p
        return best