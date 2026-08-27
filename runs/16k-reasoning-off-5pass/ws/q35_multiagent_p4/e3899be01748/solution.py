class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        digits = [int(c) for c in s]
        total = 0
        
        # For each digit d from 1 to 9, count substrings ending with d that are divisible by d
        for d in range(1, 10):
            if d == 1:
                # Every number is divisible by 1
                # Count all substrings ending in '1'
                count_1 = 0
                for i in range(n):
                    if digits[i] == 1:
                        count_1 += (i + 1)
                total += count_1
                
            elif d == 2 or d == 5:
                # For d=2: last digit is 2 (even) -> always divisible by 2
                # For d=5: last digit is 5 -> always divisible by 5
                count_d = 0
                for i in range(n):
                    if digits[i] == d:
                        count_d += (i + 1)
                total += count_d
                
            elif d == 4:
                # Divisible by 4 if last two digits form a number divisible by 4
                # We need to check s[j-1..j] for each j where s[j]=='4'
                # If j==0, then the substring is just "4", which is divisible by 4
                for j in range(n):
                    if digits[j] == 4:
                        # All substrings ending at j are valid if the last two digits form a number divisible by 4
                        # But actually, for d=4, the rule is: a number is divisible by 4 if the number formed by its last two digits is divisible by 4.
                        # So for a substring s[i..j], we need int(s[j-1..j]) % 4 == 0 (if j>=1) or if j==0, then just "4" which is divisible.
                        # Actually, if j==0, the only substring is "4", which is divisible by 4.
                        # If j>=1, then for any i <= j, the last two digits of s[i..j] are s[j-1] and s[j].
                        # So we just need to check if int(s[j-1]*s[j]) % 4 == 0.
                        if j == 0:
                            total += 1  # only substring "4"
                        else:
                            last_two = digits[j-1] * 10 + digits[j]
                            if last_two % 4 == 0:
                                total += (j + 1)  # all substrings ending at j are valid
                
            elif d == 8:
                # Divisible by 8 if last three digits form a number divisible by 8
                for j in range(n):
                    if digits[j] == 8:
                        if j < 2:
                            # For j=0: "8" -> 8%8==0 -> valid
                            # For j=1: substrings "d0d1" and "d1". 
                            #   "d1" is just "8" if j=1? No, if j=1, substrings are s[0..1] and s[1..1].
                            #   s[1..1] is "8", which is divisible by 8.
                            #   s[0..1] is two digits, which is divisible by 8 if the two-digit number is divisible by 8? 
                            #   Actually, the rule for 8 is: last three digits. If the number has fewer than 3 digits, then the whole number must be divisible by 8.
                            # So for j=0: only "8" -> valid.
                            # For j=1: 
                            #   substring s[1..1] = "8" -> valid.
                            #   substring s[0..1] = two digits, check if int(s[0..1]) % 8 == 0.
                            # For j>=2: check last three digits.
                            if j == 0:
                                total += 1
                            else: # j==1
                                # Check substring s[1..1] -> always valid
                                # Check substring s[0..1]
                                two_digit = digits[0] * 10 + digits[1]
                                if two_digit % 8 == 0:
                                    total += 2  # both substrings valid
                                else:
                                    total += 1  # only s[1..1] valid
                        else:
                            # Check last three digits
                            last_three = digits[j-2] * 100 + digits[j-1] * 10 + digits[j]
                            if last_three % 8 == 0:
                                total += (j + 1)  # all substrings ending at j are valid
                
            elif d == 6:
                # Divisible by 6 if divisible by 2 and 3.
                # Divisible by 2: last digit is 6 (even) -> always true.
                # Divisible by 3: sum of digits divisible by 3.
                # Use prefix sums of digits mod 3.
                # Precompute prefix sums mod 3
                prefix_sum = [0] * (n + 1)
                for i in range(n):
                    prefix_sum[i+1] = (prefix_sum[i] + digits[i]) % 3
                
                # For each j where digits[j]==6, count i such that (prefix_sum[j+1] - prefix_sum[i]) % 3 == 0
                # i.e., prefix_sum[i] == prefix_sum[j+1] % 3
                # We can do this in one pass
                freq = [0] * 3
                freq[0] = 1  # for prefix_sum[0]
                for j in range(n):
                    if digits[j] == 6:
                        r = prefix_sum[j+1]
                        total += freq[r]
                    # Update frequency for next iteration
                    freq[prefix_sum[j+1]] += 1
                    
            elif d in (3, 7, 9):
                # For d coprime to 10? Actually 3 and 9 are not coprime to 10, but 7 is.
                # However, the method using modular inverse of 10 mod d works only if gcd(10,d)==1.
                # For d=3 and d=9, gcd(10,d)=1? gcd(10,3)=1, gcd(10,9)=1. So yes, 10 is invertible mod 3 and mod 9.
                # So we can use the prefix sum method with modular inverse for d=3,7,9.
                
                # Compute modular inverse of 10 mod d
                inv10 = pow(10, -1, d)
                
                # We want: val(i,j) = sum_{k=i}^{j} digits[k]*10^(j-k) 
                # mod d: val(i,j) % d = (10^j % d) * (sum_{k=i}^{j} digits[k]*10^(-k)) % d
                # Let P[j] = sum_{k=0}^{j-1} digits[k]*10^(-k) mod d, with P[0]=0.
                # Then sum_{k=i}^{j} digits[k]*10^(-k) = P[j+1] - P[i] mod d.
                # Condition: (10^j % d) * (P[j+1] - P[i]) % d == 0
                # Since 10^j % d is invertible (because gcd(10,d)=1), this is equivalent to:
                # (P[j+1] - P[i]) % d == 0  => P[i] == P[j+1] % d.
                
                # Precompute powers of inv10? Actually, we can compute P[j] iteratively.
                # P[0] = 0
                # P[j+1] = P[j] + digits[j] * (inv10)^j mod d
                # But we can also compute: 
                #   Let Q[j] = digits[j] * (inv10)^j mod d
                #   Then P[j+1] = P[j] + Q[j]
                # Instead, we can maintain a running prefix sum of digits[k]*inv10^k.
                
                # Alternatively, we can compute the remainder directly:
                # Let current = 0
                # For j from 0 to n-1:
                #   current = (current + digits[j] * pow(inv10, j, d)) % d   -> but pow is expensive
                # Better: 
                #   Let term_j = digits[j] * (inv10)^j mod d
                #   We can update: term_j = term_{j-1} * inv10 mod d? 
                #   Actually, term_0 = digits[0] * 1
                #   term_1 = digits[1] * inv10
                #   term_2 = digits[2] * inv10^2 = term_1 * inv10? No, term_1 = digits[1]*inv10, then term_2 = digits[2]*inv10^2.
                #   So we can maintain a multiplier: mult = 1 initially, then mult = mult * inv10 mod d at each step.
                
                mult = 1
                freq = [0] * d
                freq[0] = 1  # for P[0]=0
                current_prefix = 0
                for j in range(n):
                    # Update multiplier for current index j: mult = inv10^j
                    # Actually, at step j, we want to add digits[j] * inv10^j
                    # So: current_prefix = (current_prefix + digits[j] * mult) % d
                    current_prefix = (current_prefix + digits[j] * mult) % d
                    mult = (mult * inv10) % d
                    
                    if digits[j] == d:
                        # We need P[i] == current_prefix for i from 0 to j
                        # The frequency array has counts for P[0] to P[j]
                        total += freq[current_prefix]
                    
                    # Update frequency for current_prefix (which is P[j+1])
                    freq[current_prefix] += 1

        return total