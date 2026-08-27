class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        ans = 0
        
        # Data structures for d=3,6
        sum_mod3 = 0
        freq3 = [0] * 3
        freq3[0] = 1
        
        # Data structures for d=7
        Q = 0
        inv10 = 5  # 10^-1 mod 7
        inv10_pow = 1
        freqQ = [0] * 7
        freqQ[0] = 1
        
        # Data structures for d=9
        sum_mod9 = 0
        freq9 = [0] * 9
        freq9[0] = 1
        
        # For tracking previous digits (needed for d=4 and d=8)
        prev1 = None  # previous digit (integer)
        prev2 = None  # digit before previous (integer)
        
        for i in range(n):
            digit_char = s[i]
            digit = int(digit_char)
            
            # d = 1, 2, 5: any substring ending with these digits is valid
            if digit_char in ('1', '2', '5'):
                ans += (i + 1)
            
            # d = 3 and d = 6 (using prefix sum mod 3)
            sum_mod3 = (sum_mod3 + digit) % 3
            if digit_char in ('3', '6'):
                ans += freq3[sum_mod3]
            freq3[sum_mod3] += 1
            
            # d = 4: depends on last two digits
            if digit_char == '4':
                if i == 0:
                    ans += 1
                else:
                    two_digit = prev1 * 10 + digit
                    if two_digit % 4 == 0:
                        ans += i + 1
                    else:
                        ans += 1
            
            # d = 7: using Q method
            inv10_pow = (inv10_pow * inv10) % 7
            Q = (Q + digit * inv10_pow) % 7
            if digit_char == '7':
                ans += freqQ[Q]
            freqQ[Q] += 1
            
            # d = 8: depends on last three digits
            if digit_char == '8':
                if i == 0:
                    ans += 1
                elif i == 1:
                    two_digit = prev1 * 10 + digit
                    if two_digit % 8 == 0:
                        ans += 2
                    else:
                        ans += 1
                else:
                    three_digit = prev2 * 100 + prev1 * 10 + digit
                    count = 0
                    if three_digit % 8 == 0:
                        count += (i - 1)  # j from 0 to i-2
                    two_digit = prev1 * 10 + digit
                    if two_digit % 8 == 0:
                        count += 1
                    count += 1  # j = i
                    ans += count
            
            # d = 9: using prefix sum mod 9
            sum_mod9 = (sum_mod9 + digit) % 9
            if digit_char == '9':
                ans += freq9[sum_mod9]
            freq9[sum_mod9] += 1
            
            # Update previous digits for next iteration
            prev2 = prev1
            prev1 = digit
        
        return ans