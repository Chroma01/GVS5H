from collections import Counter
from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0
        
        # Value compression
        val_to_idx = {val: idx for idx, val in enumerate(sorted(set(nums)))}
        m = [val_to_idx[x] for x in nums]
        K = len(val_to_idx)
        
        ans = 0
        
        def C2(x):
            return x * (x - 1) // 2
        
        for i in range(n):
            v = m[i]
            Lc = [0] * K
            Rc = [0] * K
            for j in range(i):
                Lc[m[j]] += 1
            for j in range(i + 1, n):
                Rc[m[j]] += 1
            
            Lv = Lc[v]
            Rv = Rc[v]
            Lnv = i - Lv
            Rnv = n - i - 1 - Rv
            Rsize = n - i - 1
            
            # T1: left={v,v}, all right pairs valid
            t1 = C2(Lv) * C2(Rsize)
            
            # Precompute sums over x != v
            sum_lx2 = 0          # sum l_x^2
            sum_Clx2 = 0         # sum C(l_x, 2)
            sum_lx2_rx = 0       # sum l_x^2 * r_x
            sum_lxr = 0          # sum l_x * r_x
            for x in range(K):
                if x == v:
                    continue
                lx = Lc[x]
                if lx == 0:
                    continue
                rx = Rc[x]
                sum_lx2 += lx * lx
                sum_Clx2 += C2(lx)
                sum_lx2_rx += lx * lx * rx
                sum_lxr += lx * rx
            
            # T4: left={x,y} distinct, both != v
            # H = sum_{x<y} l_x * l_y
            H = (Lnv * Lnv - sum_lx2) // 2
            # sum_{x<y} l_x*l_y*(Rnv - r_x - r_y)
            # = Rnv*H - (Lnv*sum_lxr - sum_lx2_rx)
            sum_xy_term = Rnv * H - (Lnv * sum_lxr - sum_lx2_rx)
            t4 = C2(Rv) * H + Rv * sum_xy_term
            
            # T2: left={v,x}, x != v
            # right needs >=1 v, OR both non-v and both != x
            # valid right count = C(R,2) - C(Rnv,2) + C(Rnv-rx, 2)
            #                  = Rv*Rnv + C(Rv,2) + C(Rnv-rx, 2)
            base_bracket = Rv * Rnv + C2(Rv)
            t2_inner = 0
            for x in range(K):
                if x == v:
                    continue
                lx = Lc[x]
                if lx == 0:
                    continue
                rx = Rc[x]
                bracket = base_bracket + C2(Rnv - rx)
                t2_inner += lx * bracket
            t2 = Lv * t2_inner
            
            # T3: left={x,x}, x != v, only right={v,v} valid
            t3 = C2(Rv) * sum_Clx2
            
            total_i = t1 + t2 + t3 + t4
            ans = (ans + total_i) % MOD
        
        return ans