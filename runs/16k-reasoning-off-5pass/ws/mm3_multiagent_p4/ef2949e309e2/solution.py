class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        # Coordinate compression
        comp = {v: i for i, v in enumerate(sorted(set(nums)))}
        m = len(comp)
        arr = [comp[x] for x in nums]
        
        # Prefix counts: pref[i][c] = count of c in arr[0..i-1]
        pref = [[0]*m for _ in range(n+1)]
        for i in range(n):
            c = arr[i]
            for k in range(m):
                pref[i+1][k] = pref[i][k]
            pref[i+1][c] += 1
        
        inv2 = (MOD + 1) // 2  # Modular inverse of 2
        
        def C2(x):
            if x < 2: return 0
            return x * (x - 1) % MOD * inv2 % MOD
        
        def C(x, k):
            if x < k or k < 0: return 0
            if k == 0: return 1
            if k == 1: return x % MOD
            if k == 2: return C2(x)
            return 0  # only need up to 2
        
        total = 0
        for i in range(n):
            v = arr[i]
            L_v = pref[i][v]
            left_nv = i - L_v
            R_v = pref[n][v] - pref[i+1][v]
            right_nv = (n - 1 - i) - R_v
            
            # Compute sums for k=2 cases
            # S1 = sum_{c != v} L_c * R_c
            # S2 = sum_{c != v} L_c * (L_c + 1) / 2 * R_c
            # S3 = sum_{c != v} R_c * (R_c + 1) / 2 * L_c
            S1 = S2 = S3 = 0
            for c in range(m):
                if c == v: continue
                Lc = pref[i][c]
                Rc = pref[n][c] - pref[i+1][c]
                if Lc == 0 and Rc == 0: continue
                S1 = (S1 + Lc * Rc) % MOD
                S2 = (S2 + Lc * (Lc + 1) % MOD * inv2 % MOD * Rc) % MOD
                S3 = (S3 + Rc * (Rc + 1) % MOD * inv2 % MOD * Lc) % MOD
            
            # Case (0,1): a=0, b=1 -> choose 2 from left (not v) and 1 from right (not v), all distinct
            # valid_01 = C(left_nv,2)*right_nv - left_nv*S1 + S2
            valid_01 = (C2(left_nv) * right_nv - left_nv * S1 + S2) % MOD
            # Case (1,0): a=1, b=0
            valid_10 = (left_nv * C2(right_nv) - right_nv * S1 + S3) % MOD
            
            ans_i = 0
            # (0,1) and (1,0) contributions
            ans_i = (ans_i + R_v * valid_01) % MOD
            ans_i = (ans_i + L_v * valid_10) % MOD
            
            # a+b >= 2 cases
            # (0,2): C(left_nv,2) * C(R_v,2)
            ans_i = (ans_i + C2(left_nv) * C(R_v, 2)) % MOD
            # (2,0): C(L_v,2) * C(right_nv,2)
            ans_i = (ans_i + C(L_v, 2) * C2(right_nv)) % MOD
            # (1,1): L_v * left_nv * R_v * right_nv
            ans_i = (ans_i + L_v * left_nv % MOD * R_v % MOD * right_nv) % MOD
            # (2,1): C(L_v,2) * R_v * right_nv
            ans_i = (ans_i + C(L_v, 2) * R_v % MOD * right_nv) % MOD
            # (1,2): L_v * left_nv * C(R_v,2)
            ans_i = (ans_i + L_v * left_nv % MOD * C(R_v, 2)) % MOD
            # (2,2): C(L_v,2) * C(R_v,2)
            ans_i = (ans_i + C(L_v, 2) * C(R_v, 2)) % MOD
            
            total = (total + ans_i) % MOD
        
        return total