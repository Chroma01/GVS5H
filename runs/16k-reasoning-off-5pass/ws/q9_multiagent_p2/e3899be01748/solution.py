import math

class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # cnt[k] will store the number of substrings ending at the previous position
        # that have a numeric value divisible by k.
        cnt = [0] * 10
        total_count = 0
        
        for char in s:
            d = int(char)
            new_cnt = [0] * 10
            
            # We need to compute new_cnt[k] for k in 1..9
            # Condition: (prev_val * 10 + d) % k == 0
            # Equivalent to: (prev_val * 10) % k == (-d) % k
            # Let target = (-d) % k. We need to count prev_val such that (prev_val * 10) % k == target.
            
            for k in range(1, 10):
                target = (-d) % k
                g = math.gcd(10, k)
                
                # The linear congruence 10*x = target (mod k) has solutions only if target is divisible by gcd(10, k)
                if target % g != 0:
                    new_cnt[k] = 0
                else:
                    # Reduce the equation: (10/g) * x = (target/g) (mod k/g)
                    # Let m = k/g, n = 10/g. gcd(n, m) = 1.
                    # n * x = rhs (mod m)
                    # x = rhs * inv(n, m) (mod m)
                    m = k // g
                    n = 10 // g
                    rhs = target // g
                    
                    # Calculate modular inverse of n modulo m
                    # Since gcd(n, m) = 1, inverse exists.
                    inv_n = pow(n, -1, m)
                    
                    x0 = (rhs * inv_n) % m
                    
                    # The solutions for x modulo k are x0, x0 + m, x0 + 2m, ..., x0 + (g-1)m
                    count = 0
                    for t in range(g):
                        x = x0 + t * m
                        count += cnt[x]
                    new_cnt[k] = count
            
            # If the current digit is non-zero, add the count of substrings ending here
            # that are divisible by this digit to the total.
            if d != 0:
                total_count += new_cnt[d]
            
            # Update cnt for the next iteration
            cnt = new_cnt
            
        return total_count