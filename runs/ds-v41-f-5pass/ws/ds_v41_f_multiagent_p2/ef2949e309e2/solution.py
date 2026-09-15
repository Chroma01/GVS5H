from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # Coordinate compression
        vals = sorted(set(nums))
        comp = {v: i for i, v in enumerate(vals)}
        a = [comp[v] for v in nums]
        m = len(vals)

        # Precompute C(t, 2) for t up to n
        c2 = [0] * (n + 1)
        for t in range(2, n + 1):
            c2[t] = t * (t - 1) // 2

        left = [0] * m
        right = [0] * m
        for v in a:
            right[v] += 1

        ans = 0

        for i, x in enumerate(a):
            # Remove the middle element from the right side
            right[x] -= 1

            Lx = left[x]
            Rx = right[x]
            lNonx = i - Lx
            rNonx = (n - 1 - i) - Rx

            # Total frequency of x = 5
            ans += c2[Lx] * c2[Rx]

            # Total frequency of x = 4
            ans += c2[Lx] * Rx * rNonx + c2[Rx] * Lx * lNonx

            # Total frequency of x = 3
            ans += (
                c2[Lx] * c2[rNonx]
                + c2[Rx] * c2[lNonx]
                + Lx * Rx * lNonx * rNonx
            )

            # Total frequency of x = 2:
            # the three non-x values must be pairwise distinct.
            Sp = Sq = T1 = T2 = T3 = 0
            for v in range(m):
                if v == x:
                    continue
                p = left[v]
                q = right[v]
                if p == 0 and q == 0:
                    continue
                Sp += c2[p]
                Sq += c2[q]
                T1 += p * q
                T2 += p * q * q
                T3 += p * p * q

            # Extra x on the left: choose 1 left non-x and 2 right non-x, all distinct
            A = lNonx * (c2[rNonx] - Sq) - rNonx * T1 + T2
            # Extra x on the right: choose 2 left non-x and 1 right non-x, all distinct
            B = rNonx * (c2[lNonx] - Sp) - lNonx * T1 + T3

            ans += Lx * A + Rx * B
            ans %= MOD

            # Move the middle element to the left side
            left[x] += 1

        return ans % MOD