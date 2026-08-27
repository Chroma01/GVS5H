from typing import List
from collections import defaultdict
import bisect


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)

        # Normalize each pair to (u, v) with u < v.
        us = [0] * m
        vs = [0] * m
        for i, (a, b) in enumerate(conflictingPairs):
            if a < b:
                us[i], vs[i] = a, b
            else:
                us[i], vs[i] = b, a

        # Group pair indices by their larger endpoint v.
        by_v = [[] for _ in range(n + 1)]
        for i in range(m):
            by_v[vs[i]].append(i)

        # For each u, track the smallest and second-smallest v among its pairs,
        # plus the index of the pair achieving the smallest v.
        INF = n + 1
        min_v = defaultdict(lambda: INF)
        min2_v = defaultdict(lambda: INF)
        min_idx = defaultdict(lambda: -1)
        for i in range(m):
            u, v = us[i], vs[i]
            if v < min_v[u]:
                min2_v[u] = min_v[u]
                min_v[u] = v
                min_idx[u] = i
            elif v < min2_v[u]:
                min2_v[u] = v

        # gain[i] = number of additional valid subarrays if pair i is removed.
        gain = [0] * m

        cnt = defaultdict(int)  # active pair count per u (pairs with v <= r)
        active_us = []          # sorted list of distinct active u values
        base = 0                # number of valid subarrays with all pairs kept

        for r in range(1, n + 1):
            # Activate pairs whose larger endpoint equals r.
            for i in by_v[r]:
                u = us[i]
                if cnt[u] == 0:
                    bisect.insort(active_us, u)
                cnt[u] += 1

            if not active_us:
                base += r
                continue

            # L(r) = max u among pairs with v <= r.
            best = active_us[-1]
            base += r - best

            # Second-best distinct active u (0 if none).
            sec = active_us[-2] if len(active_us) >= 2 else 0

            # If exactly one active pair has u == best (so removing it removes
            # u's contribution entirely at r), removing that unique pair drops
            # L(r) from best to sec: gain (best - sec) at this r.
            if cnt[best] == 1 and r < min2_v[best]:
                gain[min_idx[best]] += best - sec

        return base + max(gain) if m > 0 else base