class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # counts[d][r] stores the number of substrings ending at the current position
        # such that the substring value modulo d is r.
        # d ranges from 1 to 9.
        counts = [[0] * 10 for _ in range(10)]
        
        total = 0
        
        for p in range(n):
            digit = int(s[p])
            
            # Update counts for all divisors d from 1 to 9
            # We need to shift remainders: new_r = (old_r * 10 + digit) % d
            # We create a temporary array to avoid using updated values from the current step
            for d in range(1, 10):
                new_counts = [0] * 10
                for r in range(10):
                    if counts[d][r] > 0:
                        new_r = (r * 10 + digit) % d
                        new_counts[new_r] += counts[d][r]
                counts[d] = new_counts
            
            # If the current digit is 0, it cannot be the last non-zero digit of a substring
            # and substrings ending with '0' are not counted based on Example 2.
            if digit == 0:
                continue
            
            mod = digit
            
            # cnt is the number of start positions 'j' such that int(s[j:p+1]) % mod == 0
            cnt = counts[mod][0]
            
            # We only count substrings ending exactly at 'p' because substrings ending with '0'
            # are excluded from the count (as verified by Example 2).
            total += cnt
            
        return total