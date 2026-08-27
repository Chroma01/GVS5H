class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        total_count = 0
        
        # Frequency arrays for prefix sums modulo 3 and 9
        # freq3[r] stores the count of prefix sums % 3 == r encountered so far
        # freq9[r] stores the count of prefix sums % 9 == r encountered so far
        freq3 = [0] * 3
        freq9 = [0] * 9
        freq3[0] = 1
        freq9[0] = 1
        
        current_sum3 = 0
        current_sum9 = 0
        
        for i in range(n):
            d = int(s[i])
            
            if d == 0:
                continue
            
            if d == 1 or d == 2 or d == 5:
                # Any number ending in 1, 2, or 5 is divisible by itself
                total_count += (i + 1)
            
            elif d == 3 or d == 6 or d == 9:
                # Divisibility by 3, 6, 9 depends on the sum of digits
                # We need sum(s[j...i]) % d == 0
                # sum(s[j...i]) = (prefix_sum[i+1] - prefix_sum[j])
                # So we need prefix_sum[j] % d == prefix_sum[i+1] % d
                
                if d == 6:
                    # Divisible by 6 iff divisible by 2 and 3.
                    # Since last digit is 6 (even), it's always divisible by 2.
                    # So we only check divisibility by 3.
                    mod_val = 3
                    target = current_sum3
                    total_count += freq3[target]
                    
                    # Update for next iteration
                    current_sum3 = (current_sum3 + d) % 3
                    freq3[current_sum3] += 1
                else:
                    # For 3 and 9, check modulo d
                    mod_val = d
                    target = current_sum9
                    total_count += freq9[target]
                    
                    # Update for next iteration
                    current_sum9 = (current_sum9 + d) % 9
                    freq9[current_sum9] += 1
            
            elif d == 4:
                # Divisible by 4 iff the number formed by last 2 digits is divisible by 4
                if i >= 1:
                    last_two = int(s[i-1:i+1])
                    if last_two % 4 == 0:
                        total_count += (i + 1)
                    else:
                        # Only the single digit '4' is divisible by 4
                        total_count += 1
                else:
                    # Single digit '4'
                    total_count += 1
            
            elif d == 8:
                # Divisible by 8 iff the number formed by last 3 digits is divisible by 8
                if i >= 2:
                    last_three = int(s[i-2:i+1])
                    if last_three % 8 == 0:
                        # If last 3 digits are divisible by 8, then any number ending with them
                        # is divisible by 8 (since 1000 is divisible by 8).
                        # This includes all substrings of length >= 3.
                        # Length 1 is always valid (8 % 8 == 0).
                        # Length 2 needs separate check.
                        # Count = 1 (len 1) + (i - 2 + 1) (len 3 to i+1) + (1 if len 2 valid else 0)
                        # Count = i + (1 if len 2 valid else 0)
                        total_count += i
                        if int(s[i-1:i+1]) % 8 == 0:
                            total_count += 1
                    else:
                        # Only the single digit '8' is guaranteed to be divisible by 8
                        total_count += 1
                elif i == 1:
                    # Check last 2 digits
                    val = int(s[0:i+1])
                    if val % 8 == 0:
                        total_count += 2
                    else:
                        total_count += 1
                else:
                    # Single digit '8'
                    total_count += 1
            
            elif d == 7:
                # No simple digit rule, iterate backwards
                current_rem = 0
                for j in range(i, -1, -1):
                    digit = int(s[j])
                    current_rem = (current_rem * 10 + digit) % d
                    if current_rem == 0:
                        total_count += 1
            
            # d == 0 is skipped above
            
        return total_count