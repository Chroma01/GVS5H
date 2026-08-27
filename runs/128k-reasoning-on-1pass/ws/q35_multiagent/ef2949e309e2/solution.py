class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        ans = 0
        
        from collections import Counter
        
        for i in range(2, n - 2):
            v = nums[i]
            L = nums[:i]
            R = nums[i+1:]
            nL = i
            nR = len(R)
            
            freqL = Counter(L)
            freqR = Counter(R)
            
            fvL = freqL[v]
            fvR = freqR[v]
            
            # Type 2: two v's
            cL2 = fvL * (fvL - 1) // 2
            cR2 = fvR * (fvR - 1) // 2
            
            # Type 3: two identical non-v's
            cL3 = sum(f * (f - 1) // 2 for f in freqL.values() if f > 1) - cL2
            cR3 = sum(f * (f - 1) // 2 for f in freqR.values() if f > 1) - cR2
            
            # Type 1: one v, one non-v
            cL1 = fvL * (nL - fvL)
            cR1 = fvR * (nR - fvR)
            
            # Type 0: two distinct non-v's
            cL0 = nL * (nL - 1) // 2 - cL1 - cL2 - cL3
            cR0 = nR * (nR - 1) // 2 - cR1 - cR2 - cR3
            
            # k >= 2 cases: no restriction on non-v elements
            term = cL1 * cR1 + cL2 * cR0 + cL0 * cR2 + cL2 * cR1 + cL1 * cR2 + cL2 * cR2
            
            # k = 1 cases: non-v elements must be distinct
            # (1, 0): L has one v, one x; R has two distinct non-v's not equal to x
            term10 = 0
            for x, fx in freqL.items():
                if x == v: continue
                fxR = freqR.get(x, 0)
                # Pairs in R type 0 containing x: fxR * (nR - fxR - fvR)
                pairs_R_x = fxR * (nR - fxR - fvR)
                valid_R = cR0 - pairs_R_x
                term10 += fvL * fx * valid_R
                
            # (0, 1): R has one v, one y; L has two distinct non-v's not equal to y
            term01 = 0
            for y, fy in freqR.items():
                if y == v: continue
                fyL = freqL.get(y, 0)
                pairs_L_y = fyL * (nL - fyL - fvL)
                valid_L = cL0 - pairs_L_y
                term01 += fvR * fy * valid_L
                
            ans += term + term10 + term01
            ans %= MOD
            
        return ans