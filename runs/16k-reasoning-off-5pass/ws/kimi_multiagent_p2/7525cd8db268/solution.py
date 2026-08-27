from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # Normalize each pair to (lo, hi) with lo < hi, bucket by hi.
        buckets = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            lo, hi = (a, b) if a < b else (b, a)
            buckets[hi].append((lo, i))

        best = 0        # max lo among active pairs (pairs with hi <= r)
        best_cnt = 0    # how many active pairs achieve `best`
        best_idx = -1   # index of one pair achieving `best`
        second = 0      # max lo among active pairs with lo < best

        baseline = 0
        gain = [0] * m

        for r in range(1, n + 1):
            for lo, i in buckets[r]:
                if lo > best:
                    second = best
                    best = lo
                    best_cnt = 1
                    best_idx = i
                elif lo == best:
                    best_cnt += 1
                elif lo > second:
                    second = lo

            # Valid subarrays ending at r: left endpoint in (best, r]
            baseline += r - best
            # If the best is achieved by exactly one pair, removing it
            # lowers the forbidden boundary from best to second at this r.
            if best_cnt == 1:
                gain[best_idx] += best - second

        return baseline + max(gain)