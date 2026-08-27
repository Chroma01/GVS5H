class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(N, S):
            if N <= 0:
                return 0
            digits = list(map(int, str(N)))
            n = len(digits)
            
            # memo[pos][current_sum][current_prod_mod_S][is_tight][is_started]
            # We use a dictionary for memoization to handle sparse states or variable S
            memo = {}
            
            def dp(pos, current_sum, current_prod_mod, is_tight, is_started):
                # If sum exceeds S, no need to proceed
                if current_sum > S:
                    return 0
                
                # Base case: all positions filled
                if pos == n:
                    # Check if we formed a positive number and conditions are met
                    if is_started and current_sum == S and current_prod_mod == 0:
                        return 1
                    return 0
                
                state = (pos, current_sum, current_prod_mod, is_tight, is_started)
                if state in memo:
                    return memo[state]
                
                limit = digits[pos] if is_tight else 9
                res = 0
                
                for d in range(0, limit + 1):
                    new_tight = is_tight and (d == limit)
                    new_started = is_started or (d != 0)
                    
                    if not new_started:
                        # Still leading zeros, sum and product remain 0 and 1 (identity)
                        # But we track product mod S as 1 only if we consider it started?
                        # Actually, if not started, the number hasn't begun.
                        # We can treat product as 1 (multiplicative identity) for calculation purposes
                        # but it doesn't matter because we only check product at the end if is_started is true.
                        # However, to keep state consistent, let's say product mod S is 1 when not started.
                        # But wait, if we multiply by 0 later, it becomes 0.
                        # Let's use a special value for product when not started? 
                        # Actually, if is_started is False, the product is effectively 1.
                        # When we place a non-zero digit, product becomes d.
                        # When we place 0 and is_started becomes True, product becomes 0.
                        # So:
                        #   if not new_started: new_prod_mod = 1 (identity)
                        #   else:
                        #       if d == 0: new_prod_mod = 0
                        #       else: new_prod_mod = (current_prod_mod * d) % S
                        # But current_prod_mod is only meaningful if is_started was True.
                        # If is_started was False and we place d=0, new_started is False, new_prod_mod should be 1.
                        # If is_started was False and we place d>0, new_started is True, new_prod_mod = d % S.
                        # If is_started was True and we place d=0, new_prod_mod = 0.
                        # If is_started was True and we place d>0, new_prod_mod = (current_prod_mod * d) % S.
                        
                        # Let's handle logic inside the loop:
                        if d == 0:
                            # Still not started
                            new_prod_mod = 1  # Identity, but won't be checked until is_started
                        else:
                            new_prod_mod = d % S
                        res += dp(pos + 1, 0, new_prod_mod, new_tight, False)
                    else:
                        if d == 0:
                            new_prod_mod = 0
                        else:
                            if not is_started:
                                # This case is handled above? No, if is_started was False and d>0, we are here.
                                # Actually, the structure above: if not new_started: ... else: ...
                                # So if we are in else, new_started is True.
                                # If is_started was False, then current_prod_mod is 1 (identity).
                                # So new_prod_mod = (1 * d) % S = d % S.
                                # If is_started was True, new_prod_mod = (current_prod_mod * d) % S.
                                if is_started:
                                    new_prod_mod = (current_prod_mod * d) % S
                                else:
                                    new_prod_mod = d % S
                        res += dp(pos + 1, current_sum + d, new_prod_mod, new_tight, True)
                
                memo[state] = res
                return res
            
            return dp(0, 0, 1, True, False)
        
        total = 0
        for S in range(1, 82):
            total += count(r, S) - count(l - 1, S)
        return total