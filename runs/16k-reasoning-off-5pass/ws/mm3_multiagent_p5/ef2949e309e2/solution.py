import math
from collections import Counter
from typing import List

MOD = 10**9 + 7

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        
        def C(k, r):
            if r < 0 or r > k:
                return 0
            if r == 0 or r == k:
                return 1
            return math.comb(k, r)
        
        def C2(k):
            """Returns C(k, 2), 0 if k < 2."""
            if k < 2:
                return 0
            return k * (k - 1) // 2
        
        total_counter = Counter(nums)
        left_counter = Counter()
        
        ans = 0
        
        for i in range(n):
            a = nums[i]
            L = i
            R = n - 1 - i
            aL = left_counter[a]
            aR = total_counter[a] - left_counter[a] - 1
            Lp = L - aL
            Rp = R - aR
            
            good = 0
            
            # Case x >= 2
            for x_l in range(0, min(2, aL) + 1):
                for x_r in range(0, min(2, aR) + 1):
                    x = x_l + x_r
                    if x >= 2:
                        ways = C(aL, x_l) * C(aR, x_r) % MOD
                        ways = ways * C(Lp, 2 - x_l) % MOD
                        ways = ways * C(Rp, 2 - x_r) % MOD
                        good = (good + ways) % MOD
            
            # Case x = 1
            sum1 = 0
            sum2 = 0
            
            for v, total_v in total_counter.items():
                if v == a:
                    continue
                cl_v = left_counter[v]
                cr_v = total_v - cl_v
                if cl_v > 0:
                    sum1 = (sum1 + cl_v * C2(Rp - cr_v)) % MOD
                if cr_v > 0:
                    sum2 = (sum2 + cr_v * C2(Lp - cl_v)) % MOD
            
            good = (good + aL * sum1) % MOD
            good = (good + aR * sum2) % MOD
            
            ans = (ans + good) % MOD
            
            left_counter[a] += 1
        
        return ans