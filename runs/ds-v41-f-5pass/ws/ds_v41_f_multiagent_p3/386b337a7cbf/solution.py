from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        offset = total
        size = 2 * total + 1
        MASK = (1 << size) - 1
        idx = offset + k
        target_bit = (1 << idx) if 0 <= idx < size else 0

        # Positive-product DP: subsequences containing no zero.
        # Elements > limit can never be part of a valid positive-product
        # subsequence (product would be >= x > limit).
        pos_nums = [x for x in nums if x != 0 and x <= limit]
        dp = [[0] * (limit + 1) for _ in range(2)]
        active = [set(), set()]

        for x in pos_nums:
            ndp = [dp[0][:], dp[1][:]]
            nactive = [set(active[0]), set(active[1])]

            # Start a new non-empty subsequence at this element.
            ndp[1][x] |= (1 << (offset + x))
            nactive[1].add(x)

            for par in (0, 1):
                newpar = 1 - par
                bits_list = dp[par]
                for p in active[par]:
                    np = p * x
                    if np > limit:
                        continue  # monotonic: never shrinks again
                    bits = bits_list[p]
                    shifted = (bits << x) & MASK if par == 0 else bits >> x
                    if shifted:
                        ndp[newpar][np] |= shifted
                        nactive[newpar].add(np)

            dp = ndp
            active = nactive

        if target_bit:
            for p in range(limit, 0, -1):
                if (dp[0][p] & target_bit) or (dp[1][p] & target_bit):
                    return p

        # Zero-product case: subsequence must contain at least one zero.
        if target_bit and (0 in nums):
            dpz = [[0, 0], [0, 0]]
            dpz[0][0] = 1 << offset  # empty subsequence seed
            for x in nums:
                newz = [[dpz[0][0], dpz[0][1]], [dpz[1][0], dpz[1][1]]]
                for used in (0, 1):
                    for par in (0, 1):
                        bits = dpz[used][par]
                        if not bits:
                            continue
                        shifted = (bits << x) & MASK if par == 0 else bits >> x
                        if shifted:
                            npar = par ^ 1
                            nused = 1 if x == 0 else used
                            newz[nused][npar] |= shifted
                dpz = newz
            if (dpz[1][0] & target_bit) or (dpz[1][1] & target_bit):
                return 0

        return -1