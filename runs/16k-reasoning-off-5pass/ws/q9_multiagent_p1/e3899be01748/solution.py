class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        total_count = 0
        
        # Frequency maps for d=3 and d=9 (logic is identical: sum of digits)
        # Key: remainder, Value: count
        # Initialize with 0:1 because prefix sum before any digit is 0
        freq3 = {0: 1}
        cur3 = 0
        
        # Frequency map for d=7
        # Key: Q value, Value: count
        # Q[k] = (prefix_sum[k] * inv(10^k)) % 7
        freq7 = {0: 1}
        cur7 = 0
        # inv_pow10_7 represents inv(10^(i+1))
        # For i=0, we need inv(10^1) = 5 (since 10*5 = 50 = 1 mod 7)
        inv_pow10_7 = 5 
        
        for i, char in enumerate(s):
            d = int(char)
            
            if d == 0:
                continue
            
            if d == 1 or d == 2 or d == 5:
                # All substrings ending at i are divisible by d
                # Because for d=1, any number is divisible.
                # For d=2, 5, 10 is divisible by d, so value % d depends only on last digit.
                total_count += (i + 1)
            else:
                # d is 3, 7, or 9
                
                # Handle d=3 and d=9
                if d == 3 or d == 9:
                    cur3 = (cur3 + d) % d
                    count = freq3.get(cur3, 0)
                    total_count += count
                    freq3[cur3] = freq3.get(cur3, 0) + 1
                
                # Handle d=7
                if d == 7:
                    cur7 = (cur7 * 10 + d) % 7
                    q_val = (cur7 * inv_pow10_7) % 7
                    count = freq7.get(q_val, 0)
                    total_count += count
                    freq7[q_val] = freq7.get(q_val, 0) + 1
                    
                    # Update inv_pow10_7 for next iteration (i+1 -> i+2)
                    # inv(10^(k+1)) = inv(10^k) * inv(10)
                    # inv(10) mod 7 is 5
                    inv_pow10_7 = (inv_pow10_7 * 5) % 7
        
        return total_count