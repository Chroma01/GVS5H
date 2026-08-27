class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(n: int) -> int:
            if n == 0:
                return 0
            s_n = str(n)
            length = len(s_n)
            total_count = 0
            
            # The maximum sum of digits for a number < 10^9 is 9 * 9 = 81.
            # We iterate over all possible target sums 's' from 1 to 81.
            for s in range(1, 82):
                # Optimization: If the maximum possible sum for a number of 'length' digits
                # is less than 's', we can skip. Max sum for length L is 9*L.
                if 9 * length < s:
                    continue
                
                # Memoization table: (index, cur_sum, cur_prod_mod, tight, started)
                memo = {}
                
                def dp(idx: int, cur_sum: int, cur_prod_mod: int, tight: bool, started: bool) -> int:
                    # Pruning: if current sum exceeds target s, this path is invalid
                    if cur_sum > s:
                        return 0
                    
                    if idx == length:
                        # Base case:
                        # 1. We must have started (number > 0)
                        # 2. Sum must be exactly s
                        # 3. Product must be divisible by s (cur_prod_mod == 0)
                        if started and cur_sum == s and cur_prod_mod == 0:
                            return 1
                        return 0
                    
                    state = (idx, cur_sum, cur_prod_mod, tight, started)
                    if state in memo:
                        return memo[state]
                    
                    limit = int(s_n[idx]) if tight else 9
                    res = 0
                    
                    for digit in range(limit + 1):
                        new_tight = tight and (digit == limit)
                        new_started = started or (digit != 0)
                        
                        if not new_started:
                            # Still processing leading zeros
                            # cur_sum remains 0
                            # cur_prod_mod remains 1 (identity for product)
                            res += dp(idx + 1, 0, 1, new_tight, False)
                        else:
                            new_sum = cur_sum + digit
                            # Update product modulo s
                            # If this is the first non-zero digit, product becomes digit % s
                            # Otherwise, multiply previous product by digit
                            if not started:
                                new_prod_mod = digit % s
                            else:
                                new_prod_mod = (cur_prod_mod * digit) % s
                            
                            res += dp(idx + 1, new_sum, new_prod_mod, new_tight, True)
                    
                    memo[state] = res
                    return res

                total_count += dp(0, 0, 1, True, False)
            
            return total_count

        return count(r) - count(l - 1)