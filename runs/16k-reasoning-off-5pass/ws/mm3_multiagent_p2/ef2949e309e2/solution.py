from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute binomial coefficients
        C = [[0]*(n+1) for _ in range(n+1)]
        for i in range(n+1):
            C[i][0] = 1
            for j in range(1, i+1):
                C[i][j] = (C[i-1][j-1] + C[i-1][j]) % MOD
        
        def comb(x, y):
            if y < 0 or y > x: return 0
            return C[x][y]
        
        ans = 0
        for i in range(n):
            v = nums[i]
            L = i
            R = n - 1 - i
            
            # Build freqL and freqR
            freqL = {}
            freqR = {}
            for j in range(L):
                freqL[nums[j]] = freqL.get(nums[j], 0) + 1
            for j in range(i+1, n):
                freqR[nums[j]] = freqR.get(nums[j], 0) + 1
            
            vl = freqL.get(v, 0)
            vr = freqR.get(v, 0)
            
            # Sums over x != v for left side
            sumC2L_nonv = 0
            for x, c in freqL.items():
                if x == v: continue
                sumC2L_nonv += comb(c, 2)
            
            # Sums over x != v for right side
            sumC2R_nonv = 0
            for x, c in freqR.items():
                if x == v: continue
                sumC2R_nonv += comb(c, 2)
            
            # sum over x!=v of freqL[x]*freqR[x]
            sumProd_nonv = 0
            for x in freqL:
                if x == v: continue
                sumProd_nonv += freqL[x] * freqR.get(x, 0)
            
            # sum over x!=v of C(freqL[x],2)*freqR[x]
            sumC2L_prod_R_nonv = 0
            for x, c in freqL.items():
                if x == v: continue
                sumC2L_prod_R_nonv += comb(c, 2) * freqR.get(x, 0)
            
            # sum over x!=v of freqL[x]*C(freqR[x],2)
            sumC2R_prod_L_nonv = 0
            for x, c in freqR.items():
                if x == v: continue
                sumC2R_prod_L_nonv += freqL.get(x, 0) * comb(c, 2)
            
            # pick2L_nonv_distinct: 2 from left, non-v, distinct values
            pick2L_nonv_distinct = comb(L - vl, 2) - sumC2L_nonv
            pick2R_nonv_distinct = comb(R - vr, 2) - sumC2R_nonv
            
            # pick1L_1R_nonv_distinct: 1 from left (non-v), 1 from right (non-v), distinct values
            pick1L_1R_nonv_distinct = (L - vl) * (R - vr) - sumProd_nonv
            
            # pick3L_nonv_distinct: 3 from left, all non-v, all distinct values
            # Bad selections: those with >=2 of same value x
            # For value x with count c: C(c,2)*(L-vl-c) + C(c,3)
            sum_bad_3L = 0
            for x, c in freqL.items():
                if x == v: continue
                sum_bad_3L += comb(c, 2) * ((L - vl) - c) + comb(c, 3)
            pick3L_nonv_distinct = comb(L - vl, 3) - sum_bad_3L
            
            sum_bad_3R = 0
            for x, c in freqR.items():
                if x == v: continue
                sum_bad_3R += comb(c, 2) * ((R - vr) - c) + comb(c, 3)
            pick3R_nonv_distinct = comb(R - vr, 3) - sum_bad_3R
            
            # k=4: all 4 chosen are v
            k4 = comb(vl, 2) * comb(vr, 2) % MOD
            
            # k=3: 3 v's + 1 non-v
            ways_3v = comb(vl, 2) * vr + vl * comb(vr, 2)
            ways_1nonv = (L - vl) + (R - vr)
            k3 = ways_3v * ways_1nonv % MOD
            
            # k=2: 2 v's + 2 non-v's (the 2 non-v must have distinct values)
            ways_2v = comb(vl, 2) + vl * vr + comb(vr, 2)
            ways_2nonv_distinct = pick2L_nonv_distinct + pick1L_1R_nonv_distinct + pick2R_nonv_distinct
            k2 = ways_2v * ways_2nonv_distinct % MOD
            
            # k=1: 1 v + 3 non-v's (all 3 non-v must have distinct values)
            # But we must respect the 2-left/2-right split constraint!
            # Case A: v is in L. Then left = 1v + 1nonv, right = 2nonv (distinct)
            # Case B: v is in R. Then left = 2nonv (distinct), right = 1v + 1nonv
            
            # Case A: pick v position from left (vl ways), pick 1 non-v from left, pick 2 distinct non-v from right
            # Need the 1 left non-v value != both 2 right non-v values
            # For left value x: bad right pairs containing x = freqR[x] * ((R-vr) - freqR[x])
            corr_A = 0
            for x, fl in freqL.items():
                if x == v: continue
                fr = freqR.get(x, 0)
                corr_A += fl * fr * ((R - vr) - fr)
            case_A = (L - vl) * pick2R_nonv_distinct - corr_A
            k1_A = vl * case_A
            
            # Case B: pick v position from right (vr ways), pick 2 distinct non-v from left, pick 1 non-v from right
            # Need the 1 right non-v value != both 2 left non-v values
            # For right value x: bad left pairs containing x = freqL[x] * ((L-vl) - freqL[x])
            corr_B = 0
            for x, fr in freqR.items():
                if x == v: continue
                fl = freqL.get(x, 0)
                corr_B += fl * ((L - vl) - fl) * fr
            case_B = pick2L_nonv_distinct * (R - vr) - corr_B
            k1_B = vr * case_B
            
            k1 = (k1_A + k1_B) % MOD
            
            good_i = (k1 + k2 + k3 + k4) % MOD
            ans = (ans + good_i) % MOD
        
        return ans


# Verification
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1: all same, expected 6
    print("Example 1:", sol.subsequencesWithMiddleMode([1,1,1,1,1,1]))  # 6
    
    # Example 2: mixed, expected 4
    print("Example 2:", sol.subsequencesWithMiddleMode([1,2,2,3,3,4]))  # 4
    
    # Example 3: all distinct, expected 0
    print("Example 3:", sol.subsequencesWithMiddleMode([0,1,2,3,4,5,6,7,8]))  # 0
    
    # Edge: n=5, all same
    print("n=5 all same:", sol.subsequencesWithMiddleMode([1,1,1,1,1]))  # 1
    
    # Edge: n=5, all distinct
    print("n=5 all distinct:", sol.subsequencesWithMiddleMode([1,2,3,4,5]))  # 0
    
    # Edge: n=5, middle appears 3 times
    # [1,2,2,2,3] - middle is 2, which appears 3 times
    # Only 1 subsequence: pick all 5, middle is 2 (unique mode). Count=1.
    print("[1,2,2,2,3]:", sol.subsequencesWithMiddleMode([1,2,2,2,3]))  # 1
    
    # Edge: [1,1,1,2,3] - middle is 1, 3 times
    print("[1,1,1,2,3]:", sol.subsequencesWithMiddleMode([1,1,1,2,3]))  # 1
    
    # Edge: [1,2,1,3,1] - middle is 1
    # Subsequence: pick all 5, middle=1, count=3, others=1. Unique mode. Count=1.
    print("[1,2,1,3,1]:", sol.subsequencesWithMiddleMode([1,2,1,3,1]))  # 1
    
    # Edge: [1,2,3,4,5] - all distinct, no unique mode
    print("[1,2,3,4,5]:", sol.subsequencesWithMiddleMode([1,2,3,4,5]))  # 0
    
    # Larger test
    print("[1,1,2,2,3,3,4]:", sol.subsequencesWithMiddleMode([1,1,2,2,3,3,4]))
    
    # [1,1,1,1,2,2,2] - n=7
    # Middle 1 (at idx 2): need 2 from {0,1} (both 1) and 2 from {4,5,6} (values 2,2,2)
    # k=4: C(2,2)*C(0,2)=0
    # k=3: C(2,2)*0 + 2*C(0,2) = 0
    # k=2: (C(2,2)+0+0) * ways_2nonv_distinct. ways_2nonv = pick2R_nonv = C(3,2)-C(3,2)=0. So 0.
    # k=1: vl=2, vr=0. case_A only. (L-vl)*pick2R_nonv - corr = 0*0-0=0. So 0.
    # Middle 2 (at idx 4): L=4, R=2. vl=0, vr=2. 
    # k=4: 0. k=3: 0. k=2: 0. k=1: vr=2, case_B. pick2L_nonv = C(4,2)-C(3,2)=6-3=3. (R-vr)=0. So 0.
    # All others: vl=vr=0, k=1=0.
    # Total: 0
    print("[1,1,1,1,2,2,2]:", sol.subsequencesWithMiddleMode([1,1,1,1,2,2,2]))  # 0