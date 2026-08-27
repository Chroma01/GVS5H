from typing import List
from collections import defaultdict

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        n = len(nums)

        # Helper: binomial coefficient C(x, 2)
        def comb2(x: int) -> int:
            return x * (x - 1) // 2 if x >= 2 else 0

        # left_counts: frequencies of values in positions < i
        # right_counts: frequencies of values in positions > i
        left_counts = defaultdict(int)
        right_counts = defaultdict(int)
        for x in nums:
            right_counts[x] += 1

        ans = 0

        for i in range(n):
            v = nums[i]

            # Move the current element from the right side to the "processed" side
            right_counts[v] -= 1
            if right_counts[v] == 0:
                del right_counts[v]

            # Basic counts
            Lv = left_counts.get(v, 0)          # v on the left
            Rv = right_counts.get(v, 0)         # v on the right
            Lnv = i - Lv                       # non‑v on the left
            Rnv = (n - 1 - i) - Rv             # non‑v on the right

            # Sum of squares of frequencies (including v)
            sumL2 = 0
            for cnt in left_counts.values():
                sumL2 += cnt * cnt
            sumR2 = 0
            for cnt in right_counts.values():
                sumR2 += cnt * cnt

            # Exclude the value v from the sums
            sumL2_excl = sumL2 - Lv * Lv
            sumR2_excl = sumR2 - Rv * Rv

            # Number of unordered pairs of non‑v positions with distinct values
            A = (Lnv * Lnv - sumL2_excl) // 2
            Ap = (Rnv * Rnv - sumR2_excl) // 2

            # Auxiliary sums for the c = 2 cases
            B = 0
            Bp = 0
            for w, cntL in left_counts.items():
                if w == v:
                    continue
                cntR = right_counts.get(w, 0)
                if cntR == 0:
                    continue
                B += cntL * cntR * (Lnv - cntL)
                Bp += cntL * cntR * (Rnv - cntR)

            # ----- contributions for the six possible (l,r) distributions -----
            # c = 5
            c5 = comb2(Lv) * comb2(Rv)

            # c = 4
            c4 = (Lv * comb2(Rv) * Lnv) + (comb2(Lv) * Rv * Rnv)

            # c = 3
            c3 = (comb2(Lnv) * comb2(Rv)) + (comb2(Lv) * comb2(Rnv)) \
                 + (Lv * Lnv * Rv * Rnv)

            # c = 2
            term1 = Rv * (Rnv * A - B)   # (l = 0, r = 1)
            term2 = Lv * (Lnv * Ap - Bp) # (l = 1, r = 0)
            c2 = term1 + term2

            ans = (ans + c5 + c4 + c3 + c2) % MOD

            # Finally add the current element to the left side for the next iteration
            left_counts[v] += 1

        return ans