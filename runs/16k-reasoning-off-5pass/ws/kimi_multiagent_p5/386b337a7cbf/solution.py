from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        total = sum(nums)
        # Alternating sum is bounded by sum of all values in absolute value.
        if k > total or k < -total:
            return -1

        offset = total
        width = 2 * total + 1
        mask = (1 << width) - 1
        OVER = limit + 1  # sentinel for product > limit

        # layers[parity][product] = bitset over (sum + offset) of reachable
        # NON-EMPTY subsequences whose next position has the given parity.
        layers = [dict(), dict()]

        for v in nums:
            # Snapshot current states so each element is used at most once.
            snap = [dict(d) for d in layers]
            nxt = [dict(d) for d in layers]  # carry over "skip" states

            for parity in (0, 1):
                src = snap[parity]
                dst = nxt[1 - parity]
                for p, bits in src.items():
                    if p == OVER:
                        q = 0 if v == 0 else OVER
                    else:
                        q = p * v
                        if q > limit:
                            q = OVER
                    if parity == 0:
                        # next pick sits at an even index: sum += v
                        shifted = (bits << v) & mask
                    else:
                        # next pick sits at an odd index: sum -= v
                        shifted = bits >> v
                    if shifted:
                        dst[q] = dst.get(q, 0) | shifted

            # Take v as the first (and only) element: index 0 is even,
            # so sum = v, next parity = 1 (odd), product = v.
            q0 = v if v <= limit else OVER
            bit = 1 << (v + offset)
            d1 = nxt[1]
            d1[q0] = d1.get(q0, 0) | bit

            layers = nxt

        target = k + offset
        probe = 1 << target
        for p in range(limit, -1, -1):
            if (layers[0].get(p, 0) & probe) or (layers[1].get(p, 0) & probe):
                return p
        return -1