from typing import List
from collections import defaultdict

MOD = 10**9 + 7


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        for i in range(2, n - 2):
            v = nums[i]
            left = nums[:i]
            right = nums[i + 1:]
            L = len(left)
            R = len(right)

            fl = defaultdict(int)
            for x in left:
                fl[x] += 1
            fr = defaultdict(int)
            for x in right:
                fr[x] += 1

            flv = fl[v]
            frv = fr[v]
            Lp = L - flv          # left count excluding v
            Rp = R - frv          # right count excluding v

            # aggregates excluding v
            E = 0    # sum fl*fr
            Q = 0    # sum fl^2 * fr^2
            U = 0    # sum fl * fr^2
            W = 0    # sum fr * fl^2
            DLp = 0  # left distinct-valued pairs, values != v
            DRp = 0  # right distinct-valued pairs, values != v
            for x in fl:
                if x == v:
                    continue
                a = fl[x]
                b = fr[x]
                E += a * b
                Q += a * a * b * b
                U += a * b * b
                W += b * a * a
                DLp += a * (Lp - a)
            DLp //= 2
            for x in fr:
                if x == v:
                    continue
                b = fr[x]
                DRp += b * (Rp - b)
            DRp //= 2

            # k = 2: exactly two outer picks equal v (v total = 3, always valid)
            k2 = (flv * (flv - 1) // 2) * (frv * (frv - 1) // 2)
            k2 += (flv * (flv - 1) // 2) * frv * Rp
            k2 += flv * Lp * (frv * (frv - 1) // 2)
            k2 += flv * Lp * frv * Rp

            # k = 1: exactly one outer pick equals v (v total = 2)
            # left = {v, x}, right = {y, z}, y != z, x not in {y,z}, all != v
            k1 = flv * (Lp * DRp - (Rp * E - U))
            # right = {v, x}, left = {y, z}, y != z, x not in {y,z}, all != v
            k1 += frv * (Rp * DLp - (Lp * E - W))

            # k = 0: no outer pick equals v (v total = 1); all four values distinct
            k0 = DLp * DRp - (E * E - Q) // 2

            ans = (ans + k0 + k1 + k2) % MOD
        return ans