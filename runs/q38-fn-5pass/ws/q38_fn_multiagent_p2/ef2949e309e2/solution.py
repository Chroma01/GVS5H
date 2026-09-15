from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)

        # Coordinate compression.
        comp = {}
        arr = []
        for v in nums:
            if v not in comp:
                comp[v] = len(comp)
            arr.append(comp[v])

        m = len(comp)
        left = [0] * m
        right = [0] * m
        for x in arr:
            right[x] += 1

        sumsq_left = 0
        sumsq_right = sum(f * f for f in right)

        # C2[t] = number of unordered pairs from t positions.
        c2 = [i * (i - 1) // 2 for i in range(n + 1)]

        ans = 0
        rng = range(m)

        for i, x in enumerate(arr):
            # Current index is the middle, so remove it from the right side.
            old = right[x]
            new = old - 1
            right[x] = new
            sumsq_right += new * new - old * old

            ln = i
            rn = n - i - 1

            # Need at least two elements on each side.
            if ln >= 2 and rn >= 2:
                lx = left[x]
                rx = new

                # Pair counts by number of copies of x on each side.
                L0 = c2[ln - lx]
                L1 = lx * (ln - lx)
                L2 = c2[lx]

                R0 = c2[rn - rx]
                R1 = rx * (rn - rx)
                R2 = c2[rx]

                # If the four side elements contain at least two x's,
                # the middle value is automatically the unique mode.
                ans += (
                    L0 * R2 + L1 * R1 + L2 * R0 +
                    L1 * R2 + L2 * R1 + L2 * R2
                )

                # Exactly one side x: left supplies it.
                # The right pair must have two distinct values, neither x nor y.
                if lx and rn - rx >= 2:
                    M = rn - rx
                    totalD = (M * M - (sumsq_right - rx * rx)) // 2
                    s = 0
                    l = left
                    r = right
                    for y in rng:
                        if y == x:
                            continue
                        ly = l[y]
                        if ly:
                            ry = r[y]
                            s += ly * (totalD - ry * (M - ry))
                    ans += lx * s

                # Exactly one side x: right supplies it.
                # The left pair must have two distinct values, neither x nor y.
                if rx and ln - lx >= 2:
                    M = ln - lx
                    totalD = (M * M - (sumsq_left - lx * lx)) // 2
                    s = 0
                    l = left
                    r = right
                    for y in rng:
                        if y == x:
                            continue
                        ry = r[y]
                        if ry:
                            ly = l[y]
                            s += ry * (totalD - ly * (M - ly))
                    ans += rx * s

            ans %= MOD

            # Move current index to the left side for future middles.
            old = left[x]
            new = old + 1
            left[x] = new
            sumsq_left += new * new - old * old

        return ans