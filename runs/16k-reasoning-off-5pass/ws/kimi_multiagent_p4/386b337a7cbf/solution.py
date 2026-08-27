from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        OVER = limit + 1  # sentinel: product exceeds limit

        # dp[parity][alt_sum] = set of achievable products (capped at OVER),
        # considering only NON-EMPTY subsequences.
        # parity = number of picked elements mod 2
        #          (the next picked element is added if parity == 0, subtracted if parity == 1)
        dp = [dict(), dict()]

        for x in nums:
            # Snapshot current states so each element is used at most once.
            snap = [{s: set(ps) for s, ps in dp[p].items()} for p in (0, 1)]

            # Option 1: start a new subsequence with x alone.
            # Alternating sum = x, parity becomes 1, product = x (capped).
            first = dp[1].setdefault(x, set())
            first.add(x if x <= limit else OVER)

            # Option 2: append x to an existing (non-empty) subsequence.
            for parity in (0, 1):
                nxt_parity = parity ^ 1
                delta = x if parity == 0 else -x
                for s, prods in snap[parity].items():
                    ns = s + delta
                    target = dp[nxt_parity].setdefault(ns, set())
                    for p in prods:
                        if x == 0:
                            np = 0  # true product is finite, finite * 0 == 0 (even from OVER)
                        elif p >= OVER:
                            np = OVER
                        else:
                            q = p * x
                            np = q if q <= limit else OVER
                        target.add(np)

        best = -1
        for parity in (0, 1):
            for p in dp[parity].get(k, ()):
                if p <= limit and p > best:
                    best = p
        return best