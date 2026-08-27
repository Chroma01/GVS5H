class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        total_count = 0
        
        # Precompute prefix values modulo 7 for the d=7 case
        # prefix_val_7[x] stores the value of s[0...x-1] % 7
        prefix_val_7 = [0] * (n + 1)
        current_val = 0
        for i in range(n):
            digit = int(s[i])
            current_val = (current_val * 10 + digit) % 7
            prefix_val_7[i+1] = current_val
            
        # Modular inverse map for powers of 10 modulo 7
        # 10^1 = 3, inv(3) = 5
        # 10^2 = 2, inv(2) = 4
        # 10^3 = 6, inv(6) = 6
        # 10^4 = 4, inv(4) = 2
        # 10^5 = 5, inv(5) = 3
        # 10^6 = 1, inv(1) = 1
        inv_map_7 = {1: 5, 2: 4, 3: 6, 4: 2, 5: 3, 0: 1}
        
        # Frequency table for d=7: count[r][rem] = number of indices x such that
        # x % 6 == r and prefix_val_7[x] == rem
        count_7 = [[0] * 7 for _ in range(6)]
        # Initialize with x=0: prefix_val_7[0] = 0, 0 % 6 = 0
        count_7[0][0] = 1
        
        # Frequency arrays for digit sum cases (d=3, 6, 9)
        freq_3 = [0] * 3
        freq_6 = [0] * 6
        freq_9 = [0] * 9
        
        # Initialize prefix sums for digit sum cases (P[0] = 0)
        freq_3[0] = 1
        freq_6[0] = 1
        freq_9[0] = 1
        
        # Current prefix sums modulo 3, 6, 9
        curr_sum_3 = 0
        curr_sum_6 = 0
        curr_sum_9 = 0
        
        for i in range(n):
            d = int(s[i])
            
            if d == 0:
                # Update sums for future checks even if d=0
                curr_sum_3 = (curr_sum_3 + d) % 3
                curr_sum_6 = (curr_sum_6 + d) % 6
                curr_sum_9 = (curr_sum_9 + d) % 9
                continue
            
            if d == 1 or d == 2 or d == 5:
                # All substrings ending at i are valid
                total_count += (i + 1)
            
            elif d == 3 or d == 6 or d == 9:
                # Divisibility depends on sum of digits.
                # Condition: sum(s[j...i]) % d == 0
                # Equivalent to: (P[i+1] - P[j]) % d == 0 => P[j] == P[i+1] % d
                # curr_sum_d holds P[i+1] % d
                
                if d == 3:
                    total_count += freq_3[curr_sum_3]
                    freq_3[curr_sum_3] += 1
                elif d == 6:
                    total_count += freq_6[curr_sum_6]
                    freq_6[curr_sum_6] += 1
                elif d == 9:
                    total_count += freq_9[curr_sum_9]
                    freq_9[curr_sum_9] += 1
                
                # Update sums for next iteration
                curr_sum_3 = (curr_sum_3 + d) % 3
                curr_sum_6 = (curr_sum_6 + d) % 6
                curr_sum_9 = (curr_sum_9 + d) % 9

            elif d == 4:
                # Divisibility by 4 depends on last 2 digits
                valid_count = 0
                if i == 0:
                    if d % 4 == 0:
                        valid_count = 1
                else:
                    last_two = int(s[i-1:i+1])
                    if last_two % 4 == 0:
                        valid_count = i # All j from 0 to i-1 are valid
                    else:
                        if d % 4 == 0:
                            valid_count = 1 # Only j=i is valid
                total_count += valid_count
                
            elif d == 8:
                # Divisibility by 8 depends on last 3 digits
                valid_count = 0
                if i < 2:
                    if d % 8 == 0:
                        valid_count = 1
                    if i == 1:
                        if int(s[i-1:i+1]) % 8 == 0:
                            valid_count += 1
                else:
                    last_three = int(s[i-2:i+1])
                    if last_three % 8 == 0:
                        valid_count = i - 1 # All j from 0 to i-2 are valid
                    else:
                        if int(s[i-1:i+1]) % 8 == 0:
                            valid_count += 1 # j = i-1
                        if d % 8 == 0:
                            valid_count += 1 # j = i
                total_count += valid_count
            
            elif d == 7:
                current_val_i = prefix_val_7[i+1]
                count = 0
                for r in range(6):
                    k_mod = r
                    inv_val = inv_map_7[k_mod]
                    target_rem = (current_val_i * inv_val) % 7
                    idx = (i + 1 - r) % 6
                    count += count_7[idx][target_rem]
                total_count += count
                
                # Update count_7 table
                pos_mod = (i + 1) % 6
                count_7[pos_mod][current_val_i] += 1

        return total_count