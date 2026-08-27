from typing import List
from collections import Counter

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        max_sum = n * 12  # max possible |alternating sum|
        if k > max_sum or k < -max_sum:
            return -1

        counts = Counter(nums)

        # dp[(s, p)] = set of achievable products (<= limit) with alternating
        # sum s and subsequence-length parity p. Includes the empty subsequence
        # state (0,0) -> {1} which persists across groups (choosing j=0 copies).
        dp = {(0, 0): {1}}
        # dp2[(s, p)] = same, but only for NON-EMPTY subsequences.
        dp2 = {}

        for v, c in counts.items():
            new_dp = {key: set(val) for key, val in dp.items()}
            new_dp2 = {key: set(val) for key, val in dp2.items()}

            # Transitions from non-empty states: stay non-empty.
            for (s, p), prods in list(dp2.items()):
                for j in range(1, c + 1):
                    if j % 2 == 0:
                        contrib = 0
                    else:
                        contrib = v if p == 0 else -v
                    ns = s + contrib
                    if ns > max_sum or ns < -max_sum:
                        continue
                    np_ = p ^ (j & 1)
                    key = (ns, np_)
                    tgt = new_dp.setdefault(key, set())
                    tgt2 = new_dp2.setdefault(key, set())
                    if v == 0:
                        for prod in prods:
                            tgt.add(0)
                            tgt2.add(0)
                    else:
                        pwr = v ** j
                        for prod in prods:
                            nprod = prod * pwr
                            if nprod <= limit:
                                tgt.add(nprod)
                                tgt2.add(nprod)

            # Transition from the empty state (persists until used): picking
            # j >= 1 copies seeds a non-empty state. p == 0 here.
            if (0, 0) in dp and 1 in dp[(0, 0)]:
                for j in range(1, c + 1):
                    contrib = v if j % 2 == 1 else 0
                    ns = contrib
                    if ns > max_sum or ns < -max_sum:
                        continue
                    np_ = j & 1
                    key = (ns, np_)
                    tgt = new_dp.setdefault(key, set())
                    tgt2 = new_dp2.setdefault(key, set())
                    if v == 0:
                        tgt.add(0)
                        tgt2.add(0)
                    else:
                        pwr = v ** j
                        if pwr <= limit:
                            tgt.add(pwr)
                            tgt2.add(pwr)

            dp = new_dp
            dp2 = new_dp2

        best = -1
        for p in (0, 1):
            prods = dp2.get((k, p))
            if prods:
                m = max(prods)
                if m > best:
                    best = m
        return best