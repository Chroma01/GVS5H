from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0
        
        # Compress values to indices 0..V-1
        vals = sorted(set(nums))
        V = len(vals)
        val_to_idx = {v: i for i, v in enumerate(vals)}
        idx = [val_to_idx[v] for v in nums]
        
        # Total counts for each value
        total = [0] * V
        for i in idx:
            total[i] += 1
        
        # left[v] will hold count of value v in nums[0..i-1] for current middle i
        left = [0] * V
        # Initialize with first two elements (since i starts at 2)
        if n >= 2:
            left[idx[0]] += 1
            left[idx[1]] += 1
        
        ans = 0
        
        # Helper for binomial coefficients up to 2
        def comb(c, k):
            if k == 0:
                return 1
            if k == 1:
                return c
            if k == 2:
                return c * (c - 1) // 2
            return 0
        
        # Iterate over each possible middle index
        for i in range(2, n - 2):
            mid = idx[i]
            L_mid = left[mid]          # copies of mid value to the left
            R_mid = total[mid] - L_mid - 1  # copies of mid value to the right
            
            # Build polynomial product over v != mid
            # poly[a][b] = ways to pick a distinct other values on left, b on right
            poly = [[0] * 3 for _ in range(3)]
            poly[0][0] = 1
            
            for v in range(V):
                if v == mid:
                    continue
                L = left[v]
                R = total[v] - left[v]  # since v != mid, no middle subtraction
                if L == 0 and R == 0:
                    continue
                # Update poly by multiplying with (1 + L*x + R*y)
                new = [[0] * 3 for _ in range(3)]
                for a in range(3):
                    for b in range(3):
                        if poly[a][b] == 0:
                            continue
                        # not pick v
                        new[a][b] = (new[a][b] + poly[a][b]) % MOD
                        # pick v on left
                        if a + 1 < 3 and L > 0:
                            new[a+1][b] = (new[a+1][b] + poly[a][b] * L) % MOD
                        # pick v on right
                        if b + 1 < 3 and R > 0:
                            new[a][b+1] = (new[a][b+1] + poly[a][b] * R) % MOD
                poly = new
            
            # Sum over a,b choices for middle value on sides (a+b >= 1)
            for a in range(3):
                for b in range(3):
                    if a + b < 1:
                        continue
                    if a > L_mid or b > R_mid:
                        continue
                    # Need exactly 2 left and 2 right total, so other left = 2-a, other right = 2-b
                    other_left = 2 - a
                    other_right = 2 - b
                    if other_left < 0 or other_right < 0:
                        continue
                    ways_mid_left = comb(L_mid, a)
                    ways_mid_right = comb(R_mid, b)
                    other_ways = poly[other_left][other_right]
                    total_ways = ways_mid_left * ways_mid_right % MOD
                    total_ways = total_ways * other_ways % MOD
                    ans = (ans + total_ways) % MOD
            
            # Update left counts: current middle becomes part of left for next iteration
            left[mid] += 1
        
        return ans