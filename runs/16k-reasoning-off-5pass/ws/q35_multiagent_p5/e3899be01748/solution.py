class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        count = 0
        
        for d in range(1, 10):
            if d == 0:
                continue
            
            import math
            if math.gcd(10, d) == 1:
                inv10 = pow(10, -1, d)
                freq = [0] * d
                inv_pow10 = 1
                P = 0
                
                for j in range(n):
                    digit = int(s[j])
                    val = (P * inv_pow10) % d
                    freq[val] += 1
                    
                    P = (P * 10 + digit) % d
                    
                    if digit == d:
                        target = (P * inv_pow10) % d
                        count += freq[target]
                    
                    inv_pow10 = (inv_pow10 * inv10) % d
            else:
                for j in range(n):
                    if int(s[j]) != d:
                        continue
                    num = 0
                    pow10 = 1
                    for i in range(j, -1, -1):
                        digit = int(s[i])
                        num = (digit * pow10 + num) % d
                        pow10 = (pow10 * 10) % d
                        if num == 0:
                            count += 1
        
        return count