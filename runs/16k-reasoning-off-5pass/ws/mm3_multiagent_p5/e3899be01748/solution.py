class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        digits = [int(c) for c in s]
        ans = 0
        
        # For each possible last digit d (1..9)
        for d in range(1, 10):
            # For each end position j where s[j] == d
            for j in range(n):
                if digits[j] != d:
                    continue
                
                # Start with the single-character substring
                val = digits[j] % d
                pow10 = 1  # 10^0 mod d
                streak = 0  # consecutive non-zero remainders
                
                if val == 0:
                    ans += 1
                else:
                    streak = 1
                
                # Scan leftward; cap at d*10 steps for safety
                limit = d * 10
                for k in range(1, min(limit, j + 1) + 1):
                    pow10 = (pow10 * 10) % d
                    val = (digits[j - k] * pow10 + val) % d
                    
                    if val == 0:
                        ans += 1
                        streak = 0
                    else:
                        streak += 1
                    
                    # Pigeonhole: if we've seen d consecutive non-zero remainders,
                    # no future extension can produce remainder 0
                    if streak >= d:
                        break
        
        return ans