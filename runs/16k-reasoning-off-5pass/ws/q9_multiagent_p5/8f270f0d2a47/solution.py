class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count(n: int) -> int:
            if n == 0:
                return 0
            
            digits = [int(d) for d in str(n)]
            num_digits = len(digits)
            total_count = 0
            
            # Maximum possible sum of digits for n < 10^9 is 9*9 = 81.
            # We iterate over all possible target sums S from 1 to 81.
            # For a fixed S, we count numbers <= n where digit_sum == S and digit_product % S == 0.
            for S in range(1, 82):
                # Memoization table for the current S
                # State: (index, tight, current_sum, current_prod_mod_S)
                memo = {}
                
                def dfs(index: int, tight: bool, current_sum: int, current_prod_mod: int) -> int:
                    # Base case: if we have processed all digits
                    if index == num_digits:
                        # Check if the sum matches the target S
                        if current_sum == S:
                            # Check if product is divisible by S
                            # current_prod_mod holds (product % S). If it is 0, then divisible.
                            return 1
                        return 0
                    
                    state = (index, tight, current_sum, current_prod_mod)
                    if state in memo:
                        return memo[state]
                    
                    limit = digits[index] if tight else 9
                    res = 0
                    
                    for d in range(limit + 1):
                        new_tight = tight and (d == limit)
                        new_sum = current_sum + d
                        
                        # Optimization: if current_sum already exceeds S, stop
                        if new_sum > S:
                            continue
                        
                        # Calculate new product modulo S
                        # If d is 0, product becomes 0. 0 % S is 0.
                        # If d is not 0, we update the modulo.
                        if d == 0:
                            new_prod_mod = 0
                        else:
                            # We need (current_prod * d) % S
                            # current_prod_mod holds (current_prod % S)
                            new_prod_mod = (current_prod_mod * d) % S
                        
                        res += dfs(index + 1, new_tight, new_sum, new_prod_mod)
                    
                    memo[state] = res
                    return res
                
                # Start DFS
                # index=0, tight=True, current_sum=0, current_prod_mod=1 (identity for multiplication)
                # Note: current_prod_mod=1 is correct because if the first non-zero digit is d, 
                # then product becomes d, and d % S = (1 * d) % S.
                # If the number is 0 (all digits 0), sum is 0, which is not in range [1, 81], so it won't be counted.
                total_count += dfs(0, True, 0, 1)
            
            return total_count

        return count(r) - count(l - 1)