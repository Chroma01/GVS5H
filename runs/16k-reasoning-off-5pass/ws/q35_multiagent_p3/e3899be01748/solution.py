class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        total = 0
        
        # For each possible non-zero last digit d from 1 to 9
        for d in range(1, 10):
            # cnt[r] will store the number of starting positions i (<= current j)
            # such that the substring s[i..j] has remainder r modulo d
            cnt = [0] * d
            
            for j in range(n):
                digit = int(s[j])
                # Update remainders for all existing substrings ending at j-1
                # to now end at j: new_rem = (old_rem * 10 + digit) % d
                new_cnt = [0] * d
                for r in range(d):
                    if cnt[r] > 0:
                        new_rem = (r * 10 + digit) % d
                        new_cnt[new_rem] += cnt[r]
                
                # Add the new substring starting and ending at j: value is digit
                new_cnt[digit % d] += 1
                cnt = new_cnt
                
                # Add the count of substrings ending at j that are divisible by d
                # But only if the last digit of the substring is d (i.e., s[j] == d)
                if digit == d:
                    total += cnt[0]
        
        return total