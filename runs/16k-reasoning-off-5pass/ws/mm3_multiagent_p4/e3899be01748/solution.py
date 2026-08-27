class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        # Convert string to list of integers for faster access
        digits = [int(ch) for ch in s]
        ans = 0
        
        # For each possible non‑zero last digit d = 1..9
        for d in range(1, 10):
            # cnt[r] = number of previous prefix values (ending before current position)
            # that had remainder r when interpreted modulo d.
            # The virtual empty prefix (value 0) is included as cnt[0] = 1.
            cnt = [0] * d
            cnt[0] = 1
            
            val = 0          # value of the current suffix built from left to right, modulo d
            pow10 = 1        # 10^k mod d, where k is the length of the suffix built so far
            
            for j in range(n):
                cur_digit = digits[j]
                # Update the suffix value: we are appending cur_digit at the rightmost position.
                # Because we are building the number from left to right, each new character
                # corresponds to multiplying the existing value by 10 and adding the new digit.
                # In modulo arithmetic this is:
                #   new_val = (old_val * 10 + cur_digit) % d
                # The implementation uses an incremental form with pow10 to keep the
                # arithmetic clear and avoid overflow (though Python handles big ints).
                val = (val + cur_digit * pow10) % d
                
                # All earlier positions i-1 (i.e., prefixes) that have the same remainder
                # give a substring s[i..j] divisible by d.
                ans += cnt[val]
                
                # Record this remainder for future substrings.
                cnt[val] += 1
                
                # Update the power of ten for the next position.
                pow10 = (pow10 * 10) % d
        
        return ans