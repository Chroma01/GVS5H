class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self.count_upto(r) - self.count_upto(l - 1)
    
    def count_upto(self, n: int) -> int:
        if n == 0:
            return 0
        
        s_n = str(n)
        len_n = len(s_n)
        total = 0
        
        # For each possible digit sum S from 1 to 81
        for S in range(1, 82):
            # Count numbers <= n with digit sum S and product % S == 0
            total += self._count_with_sum(s_n, S, len_n)
        
        return total
    
    def _count_with_sum(self, s_n: str, S: int, len_n: int) -> int:
        memo = {}
        
        def dp(index, current_sum, current_product_mod, tight, leading_zeros):
            if index == len_n:
                # Check if we have a valid number
                if leading_zeros and current_sum == 0:
                    return 0  # This is the number 0, which is not positive
                return 1 if current_sum == S and current_product_mod == 0 else 0
            
            state = (index, current_sum, current_product_mod, tight, leading_zeros)
            if state in memo:
                return memo[state]
            
            limit = int(s_n[index]) if tight else 9
            res = 0
            
            for d in range(10):
                new_tight = tight and (d == limit)
                new_leading_zeros = leading_zeros and (d == 0)
                
                if new_leading_zeros:
                    # Still in leading zeros, sum and product remain 0 and 1
                    res += dp(index + 1, 0, 1, new_tight, True)
                else:
                    # Placing a non-zero digit or first non-zero digit
                    new_sum = current_sum + d
                    new_product_mod = (current_product_mod * d) % S
                    
                    if new_sum > S:
                        continue
                    
                    res += dp(index + 1, new_sum, new_product_mod, new_tight, False)
            
            memo[state] = res
            return res
        
        return dp(0, 0, 1, True, True)