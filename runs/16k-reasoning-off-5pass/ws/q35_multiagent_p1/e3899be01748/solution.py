class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        total = 0
        
        # For each possible non-zero last digit d from 1 to 9
        for d in range(1, 10):
            # freq[r] will store the count of substrings ending at the previous position
            # such that their value modulo d is r.
            freq = [0] * d
            
            for j in range(n):
                # Update the frequency array for the new character s[j]
                # The new remainder for a substring s[i..j] (i < j) is (old_rem * 10 + int(s[j])) % d
                # But we only care about the state when s[j] == d, and in that case int(s[j]) % d == 0.
                # However, to maintain the state correctly for future positions, we must update for all j.
                # Create a new frequency array
                new_freq = [0] * d
                digit = int(s[j])
                for r in range(d):
                    if freq[r] > 0:
                        new_rem = (r * 10 + digit) % d
                        new_freq[new_rem] += freq[r]
                
                # If the current digit is d, then substrings ending here with last digit d are candidates
                if digit == d:
                    # Add substrings s[i..j] with i < j that have remainder 0
                    total += new_freq[0]
                    # Add the single-digit substring s[j..j] which is d, and d % d == 0
                    total += 1
                
                # Update freq for the next iteration
                freq = new_freq
                
        return total