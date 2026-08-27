from math import gcd

class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        # Frequency arrays for remainders of substrings ending at the previous position
        # k can be 1,2,3,4,7,9 based on d / gcd(10,d) for d in 1..9
        freq = {
            1: [0],
            2: [0, 0],
            3: [0, 0, 0],
            4: [0, 0, 0, 0],
            7: [0] * 7,
            9: [0] * 9
        }
        ans = 0
        for j, ch in enumerate(s):
            d = int(ch)
            if d != 0:
                g = gcd(10, d)
                k = d // g
                # Add count of i < j such that s[i..j-1] mod k == 0
                ans += freq[k][0]
                # Add the single-digit substring
                ans += 1
            # Update frequency arrays for substrings ending at current position
            for k in [1, 2, 3, 4, 7, 9]:
                old = freq[k]
                new = [0] * k
                digit = d
                for r in range(k):
                    new_r = (r * 10 + digit) % k
                    new[new_r] += old[r]
                # Add the single-character substring
                new[digit % k] += 1
                freq[k] = new
        return ans