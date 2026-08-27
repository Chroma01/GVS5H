class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        # Helper function to count beautiful numbers in [1, n]
        def count_beautiful(n: int) -> int:
            if n <= 0:
                return 0
            
            digits = [int(d) for d in str(n)]
            num_digits = len(digits)
            
            # We'll use a memoized DP for each sum S from 1 to 81
            # But to avoid recomputing the same DP structure, we can define a general DP
            # that takes S as a parameter and returns count of numbers in [1, n] with digit sum S and product divisible by S.
            
            total = 0
            
            # Precompute the DP table for a given n and S
            # State: (pos, tight, current_sum, current_prod_mod_S, has_zero)
            # We'll use lru_cache or a manual memo dict
            
            for S in range(1, 82):  # S from 1 to 81
                # Memoization dictionary for the DP
                memo = {}
                
                def dp(pos: int, tight: bool, current_sum: int, current_prod_mod_S: int, has_zero: bool) -> int:
                    # If current_sum exceeds S, no need to proceed
                    if current_sum > S:
                        return 0
                    
                    # If we've placed all digits
                    if pos == num_digits:
                        # Check if sum is exactly S and product condition is met
                        if current_sum == S:
                            if has_zero:
                                # Product is 0, which is divisible by S
                                return 1
                            else:
                                # Check if product mod S is 0
                                if current_prod_mod_S == 0:
                                    return 1
                                else:
                                    return 0
                        else:
                            return 0
                    
                    state = (pos, tight, current_sum, current_prod_mod_S, has_zero)
                    if state in memo:
                        return memo[state]
                    
                    limit = digits[pos] if tight else 9
                    res = 0
                    
                    for d in range(0, limit + 1):
                        new_tight = tight and (d == limit)
                        new_has_zero = has_zero or (d == 0)
                        
                        # If we are in leading zeros and d is 0, we skip adding to sum and product
                        # But note: our DP doesn't explicitly track "leading zeros" state separately.
                        # Instead, we treat 0 as a digit. However, for the number 0 itself, it's not positive.
                        # We need to be careful: the number 0 is not counted because we start from 1.
                        # Also, leading zeros don't contribute to sum or product.
                        # How to handle leading zeros? 
                        # We can add a state variable for "started" (i.e., non-zero digit has been placed).
                        # But to keep state small, we can note that if current_sum is 0 and has_zero is False, 
                        # it means we haven't started. But if we place a 0 and haven't started, it's still leading zero.
                        # Let's add a 'started' flag.
                        pass
                    
                    # Redefine DP with 'started' flag
                    # Actually, let's redefine the DP inside the loop with 'started'
                    pass
                
                # Redefine dp with started flag
                memo2 = {}
                
                def dp2(pos: int, tight: bool, current_sum: int, current_prod_mod_S: int, has_zero: bool, started: bool) -> int:
                    if current_sum > S:
                        return 0
                    
                    if pos == num_digits:
                        if started and current_sum == S:
                            if has_zero:
                                return 1
                            else:
                                if current_prod_mod_S == 0:
                                    return 1
                                else:
                                    return 0
                        else:
                            return 0
                    
                    state = (pos, tight, current_sum, current_prod_mod_S, has_zero, started)
                    if state in memo2:
                        return memo2[state]
                    
                    limit = digits[pos] if tight else 9
                    res = 0
                    
                    for d in range(0, limit + 1):
                        new_tight = tight and (d == limit)
                        new_started = started or (d != 0)
                        new_has_zero = has_zero or (d == 0)
                        
                        # If not started and d is 0, it's a leading zero, so don't update sum or product
                        if not new_started:
                            # Leading zero, sum and product remain 0, has_zero remains False (since leading zero doesn't count as a digit 0 for product)
                            # Actually, has_zero should only be true if a non-leading zero is placed.
                            # So if not started, new_has_zero should be False.
                            new_has_zero_for_dp = False
                            new_prod_mod = current_prod_mod_S  # remains 0
                            new_sum = current_sum  # remains 0
                        else:
                            if d == 0:
                                new_has_zero_for_dp = True
                                new_prod_mod = current_prod_mod_S  # product becomes 0, but we mark has_zero
                                new_sum = current_sum  # 0 doesn't add to sum? Actually, 0 adds 0 to sum.
                                # But if started is True and d is 0, then it's a valid digit 0.
                                # Sum increases by 0, so no change.
                                new_sum = current_sum
                            else:
                                new_has_zero_for_dp = has_zero  # remains as is
                                # Update product mod S: multiply by d
                                new_prod_mod = (current_prod_mod_S * d) % S
                                new_sum = current_sum + d
                        
                        res += dp2(pos + 1, new_tight, new_sum, new_prod_mod, new_has_zero_for_dp, new_started)
                    
                    memo2[state] = res
                    return res
                
                # Start DP: pos=0, tight=True, sum=0, prod_mod=0, has_zero=False, started=False
                count_S = dp2(0, True, 0, 0, False, False)
                total += count_S
            
            return total
        
        return count_beautiful(r) - count_beautiful(l - 1)