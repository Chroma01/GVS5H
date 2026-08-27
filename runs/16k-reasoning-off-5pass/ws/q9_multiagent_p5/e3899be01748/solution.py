class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        
        # Initialize counts for moduli 3, 7, and 9.
        # c[r] stores the number of starting positions j such that 
        # the number formed by s[j:i] has remainder r modulo M.
        # Initially, for i=0, the prefix s[0:0] is empty (value 0), so remainder 0 count is 1.
        c3 = [0] * 3
        c9 = [0] * 9
        c7 = [0] * 7
        c3[0] = 1
        c9[0] = 1
        c7[0] = 1
        
        for i, ch in enumerate(s):
            d = int(ch)
            
            if d == 0:
                continue
            
            current_count = 0
            
            if d in (1, 2, 5):
                # For d=1, 2, 5, any number is divisible by d (after the 10*d logic).
                # Specifically, (val * 10 + d) % d == 0 is always true.
                # All substrings ending at i are valid.
                current_count = i + 1
            elif d in (3, 6):
                # For d=3, 6, we need val(s[j:i]) % 3 == 0.
                current_count = c3[0]
            elif d == 9:
                # For d=9, we need val(s[j:i]) % 9 == 0.
                current_count = c9[0]
            elif d == 7:
                # For d=7, we need val(s[j:i]) % 7 == 0.
                current_count = c7[0]
            elif d == 4:
                # For d=4, we need val(s[j:i]) % 2 == 0.
                # This is equivalent to checking the last 2 digits of s[j:i].
                # s[j:i] ends at i-1.
                # If length >= 2 (j <= i-2), check int(s[i-2:i]) % 4 == 0.
                # If length == 1 (j == i-1), check int(s[i-1]) % 4 == 0.
                # If length == 0 (j == i), value is 0, which is divisible.
                current_count = 1  # j = i
                if i > 0 and int(s[i-1]) % 4 == 0:
                    current_count += 1  # j = i-1
                if i >= 2 and int(s[i-2:i]) % 4 == 0:
                    current_count += i - 1  # j <= i-2
            elif d == 8:
                # For d=8, we need val(s[j:i]) % 4 == 0.
                # This is equivalent to checking the last 3 digits of s[j:i].
                # s[j:i] ends at i-1.
                # If length >= 3 (j <= i-3), check int(s[i-3:i]) % 8 == 0.
                # If length == 2 (j == i-2), check int(s[i-2:i]) % 8 == 0.
                # If length == 1 (j == i-1), check int(s[i-1]) % 8 == 0.
                # If length == 0 (j == i), value is 0.
                current_count = 1  # j = i
                if i > 0 and int(s[i-1]) % 8 == 0:
                    current_count += 1  # j = i-1
                if i >= 2 and int(s[i-2:i]) % 8 == 0:
                    current_count += 1  # j = i-2
                if i >= 3 and int(s[i-3:i]) % 8 == 0:
                    current_count += i - 2  # j <= i-3
            
            ans += current_count
            
            # Update the remainder counters for the next iteration.
            # The new value for a starting position j will be:
            # new_val = old_val * 10 + d
            # So new_rem = (old_rem * 10 + d) % M
            
            digit = d
            
            # Update c3
            new_c3 = [0] * 3
            for r in range(3):
                new_c3[(r * 10 + digit) % 3] = c3[r]
            c3 = new_c3
            
            # Update c9
            new_c9 = [0] * 9
            for r in range(9):
                new_c9[(r * 10 + digit) % 9] = c9[r]
            c9 = new_c9
            
            # Update c7
            new_c7 = [0] * 7
            for r in range(7):
                new_c7[(r * 10 + digit) % 7] = c7[r]
            c7 = new_c7
            
        return ans