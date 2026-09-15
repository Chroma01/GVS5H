from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        vals = sorted(set(nums))
        comp = {v: k for k, v in enumerate(vals)}
        arr = [comp[v] for v in nums]
        D = len(vals)

        # c2[k] = C(k, 2)
        c2 = [k * (k - 1) // 2 for k in range(n + 2)]

        left_freq = [0] * D
        right_freq = [0] * D
        for v in arr:
            right_freq[v] += 1

        S2_L = 0  # sum of C2(left_freq[v])
        S2_R = 0  # sum of C2(right_freq[v])
        for v in range(D):
            S2_R += c2[right_freq[v]]

        ans = 0
        for i in range(n):
            x = arr[i]
            # move index i out of the right side
            old = right_freq[x]
            right_freq[x] = old - 1
            S2_R -= (old - 1)

            b = old - 1                 # x's on the right of i
            a = left_freq[x]            # x's on the left of i
            nL = i
            nR = n - 1 - i
            M_L = nL - a                # non-x on the left
            M_R = nR - b                # non-x on the right

            S2_L_nonx = S2_L - c2[a]
            S2_R_nonx = S2_R - c2[b]

            LC0 = c2[M_L]; LC1 = a * M_L; LC2 = c2[a]
            RC0 = c2[M_R]; RC1 = b * M_R; RC2 = c2[b]

            # t = 1 + cL + cR >= 3 : x is automatically the unique mode
            auto = (LC2 * (RC0 + RC1 + RC2)
                    + LC1 * (RC1 + RC2)
                    + LC0 * RC2)
            ans = (ans + auto) % MOD

            # t == 2, extra x on the left: left picks 1 x + 1 non-x,
            # right picks 2 non-x with pairwise distinct values, all != left non-x value
            if a > 0 and M_R >= 2:
                s = 0
                for val in range(D):
                    if val == x:
                        continue
                    fl = left_freq[val]
                    if fl:
                        cu = right_freq[val]
                        s += fl * (c2[M_R - cu] - S2_R_nonx + c2[cu])
                ans = (ans + a * (s % MOD)) % MOD

            # t == 2, extra x on the right (symmetric)
            if b > 0 and M_L >= 2:
                s = 0
                for val in range(D):
                    if val == x:
                        continue
                    fr = right_freq[val]
                    if fr:
                        du = left_freq[val]
                        s += fr * (c2[M_L - du] - S2_L_nonx + c2[du])
                ans = (ans + b * (s % MOD)) % MOD

            # move index i into the left side
            oldL = left_freq[x]
            S2_L += oldL
            left_freq[x] = oldL + 1

        return ans % MOD