from typing import List
from collections import Counter

MOD = 10**9 + 7

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        # C(x,2) table
        c2 = [0] * (n + 1)
        for x in range(2, n + 1):
            c2[x] = x * (x - 1) // 2

        right = Counter(nums)
        left = Counter()

        ans = 0
        for i in range(n):
            v = nums[i]
            right[v] -= 1
            if right[v] == 0:
                del right[v]

            L = i
            R = n - i - 1
            if L >= 2 and R >= 2:
                lv = left.get(v, 0)
                rv = right.get(v, 0)
                l = L - lv  # non-v elements on left
                r = R - rv  # non-v elements on right

                # ---- A_{k>=2}: at least 2 extra copies of v among the 4 picks.
                # Then freq(v) >= 3 and no other value can reach 3 with <= 2
                # remaining slots, so ALL completions are good.
                A_kge2 = (
                    c2[lv] * c2[r]            # a=2,b=0
                    + c2[rv] * c2[l]          # a=0,b=2
                    + c2[lv] * rv * r         # a=2,b=1
                    + c2[rv] * lv * l         # a=1,b=2
                    + c2[lv] * c2[rv]         # a=2,b=2
                )

                # Aggregates over non-v values.
                sl = sr = 0          # sum C(lu,2), sum C(ru,2)
                p1 = 0               # sum lu*ru*(r-ru)
                q1 = 0               # sum lu*ru*(l-lu)
                for val, lu in left.items():
                    if val == v:
                        continue
                    ru = right.get(val, 0)
                    sl += c2[lu]
                    sr += c2[ru]
                    p1 += lu * ru * (r - ru)
                    q1 += lu * ru * (l - lu)

                dl = c2[l] - sl   # left 2-picks with distinct non-v values
                dr = c2[r] - sr   # right 2-picks with distinct non-v values

                # ---- A_{k=1}: exactly one extra copy of v.
                # v-copy from left: lv * (1 left non-v + 2 right distinct non-v,
                # left single's value absent from right pair) = lv*(l*dr - p1).
                # Symmetric for v-copy from right.
                A_k1 = lv * (l * dr - p1) + rv * (r * dl - q1)

                ans = (ans + A_kge2 + A_k1) % MOD

            left[v] += 1

        return ans % MOD