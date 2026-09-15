from typing import List
import bisect


class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        LIMIT = 10 ** 9

        # Base-4 blocks [4^(k-1), 4^k - 1]; every x in block k needs exactly k
        # successive floor(x/4) reductions to reach 0, i.e. c(x) = k.
        starts = []
        blocks = []
        lo, k = 1, 1
        while lo <= LIMIT:
            hi = lo * 4 - 1
            starts.append(lo)
            blocks.append((lo, hi, k))
            lo *= 4
            k += 1

        total = 0
        for l, r in queries:
            # S = sum of c(x) for x in [l, r], grouped by block.
            S = 0
            for bl, bh, bk in blocks:
                if bl > r:
                    break
                a = l if l > bl else bl
                b = r if r < bh else bh
                if a <= b:
                    S += bk * (b - a + 1)

            # c is nondecreasing, so max single-element cost over [l, r] is c(r).
            # bisect_right gives the count of block starts <= r, which equals c(r).
            mc = bisect.bisect_right(starts, r)

            # Each operation consumes two selections; the heaviest element must be
            # selected c(r) times. Lower bound max(ceil(S/2), c(r)) is achievable.
            total += max((S + 1) // 2, mc)

        return total