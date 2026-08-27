class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_upto(n, S):
            if n <= 0:
                return 0
            digits = list(map(int, str(n)))
            num_digits = len(digits)
            
            # dp(pos, current_sum, current_prod_mod_S, tight, started)
            # We use lru_cache for memoization
            from functools import lru_cache
            
            @lru_cache(maxsize=None)
            def dp(pos, current_sum, current_prod_mod_S, tight, started):
                # If current sum already exceeds S, no need to proceed
                if current_sum > S:
                    return 0
                
                # If we've placed all digits
                if pos == num_digits:
                    # Check if we have started (i.e., the number is positive)
                    # and the sum is exactly S and product is divisible by S
                    if started and current_sum == S and current_prod_mod_S == 0:
                        return 1
                    return 0
                
                limit = digits[pos] if tight else 9
                total = 0
                
                for d in range(0, limit + 1):
                    new_tight = tight and (d == limit)
                    new_started = started or (d != 0)
                    
                    if not new_started:
                        # Still leading zeros, sum and product remain 0 and 1 (but effectively not started)
                        # We pass current_sum=0, current_prod_mod_S=1 (identity) but it doesn't matter as long as started is False
                        total += dp(pos + 1, 0, 1, new_tight, False)
                    else:
                        new_sum = current_sum + d
                        # If new_sum already exceeds S, skip
                        if new_sum > S:
                            continue
                        # Update product mod S: if it's the first digit, product is d, else current_prod * d
                        if not started:
                            # First non-zero digit
                            new_prod_mod = d % S
                        else:
                            new_prod_mod = (current_prod_mod_S * d) % S
                        
                        total += dp(pos + 1, new_sum, new_prod_mod, new_tight, True)
                
                return total
            
            return dp(0, 0, 1, True, False)
        
        total = 0
        for S in range(1, 82):  # Sum of digits can be at most 9*9=81 for numbers < 10^9
            total += count_upto(r, S) - count_upto(l - 1, S)
        
        return total