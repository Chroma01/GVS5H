from typing import List


class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        S = sum(nums)
        # Any subsequence's alternating sum lies in [-S, S].
        if k < -S or k > S:
            return -1

        offset = S
        OVER = limit + 1  # sentinel: product currently exceeds limit
        # dp[parity][product] = bitset of achievable alternating sums
        # (bit offset+s represents sum s). parity = parity of the NEXT
        # picked subsequence index (0 => next pick is added, 1 => subtracted).
        # Only non-empty subsequences are stored: states are created solely
        # via singleton starts, so the invalid empty subsequence (sum 0,
        # product 1) is never represented.
        dp = [{}, {}]

        for x in nums:
            # Snapshot so x cannot be picked twice within one iteration.
            snap = [(p, prod, bits)
                    for p in (0, 1)
                    for prod, bits in dp[p].items()]
            for p, prod, bits in snap:
                nb = (bits << x) if p == 0 else (bits >> x)
                nprod = prod * x
                if nprod > limit:
                    # Keep as OVER rather than discarding: a later 0
                    # collapses any overflowed product to 0, which may be
                    # a valid answer (e.g. nums=[5,0], k=5, limit=3 -> 0).
                    # Merging all overflowed values is safe because the only
                    # escape from OVER is x==0 (-> 0 regardless of value);
                    # OVER * (>=1) stays OVER.
                    nprod = OVER
                q = 1 - p
                d = dp[q]
                d[nprod] = d.get(nprod, 0) | nb
            # Start a new singleton subsequence [x]: sum = x, next parity = 1.
            sp = x if x <= limit else OVER
            d = dp[1]
            d[sp] = d.get(sp, 0) | (1 << (offset + x))

        target = k + offset
        best = -1
        for p in (0, 1):
            for prod, bits in dp[p].items():
                # prod == 0 is a valid answer (0 > -1), distinct from "none".
                if prod <= limit and prod > best and (bits >> target) & 1:
                    best = prod
        return best