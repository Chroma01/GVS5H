class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        def count_up_to(n: int) -> int:
            if n <= 0:
                return 0
            digits = [int(d) for d in str(n)]
            num_digits = len(digits)
            total = 0
            
            # Iterate over all possible digit sums s from 1 to 81
            for s in range(1, 82):
                # Memoization table for fixed s: (pos, tight, current_sum, current_prod_mod_s)
                memo = {}
                
                def dp(pos: int, tight: bool, current_sum: int, current_prod_mod_s: int) -> int:
                    # If current sum exceeds s, no need to proceed
                    if current_sum > s:
                        return 0
                    
                    # Base case: all positions filled
                    if pos == num_digits:
                        # Check if sum is exactly s and product is divisible by s
                        if current_sum == s and current_prod_mod_s == 0:
                            return 1
                        else:
                            return 0
                    
                    state = (pos, tight, current_sum, current_prod_mod_s)
                    if state in memo:
                        return memo[state]
                    
                    limit = digits[pos] if tight else 9
                    res = 0
                    for d in range(0, limit + 1):
                        new_tight = tight and (d == limit)
                        new_sum = current_sum + d
                        # If new_sum already exceeds s, skip (optimization)
                        if new_sum > s:
                            continue
                        # Calculate new product mod s
                        # Note: if current_prod_mod_s is 0, then 0 * d % s = 0
                        new_prod_mod_s = (current_prod_mod_s * d) % s
                        res += dp(pos + 1, new_tight, new_sum, new_prod_mod_s)
                    
                    memo[state] = res
                    return res
                
                # Start DP from position 0, tight=True, sum=0, prod_mod=1 (identity for multiplication)
                # But note: for the first digit, if we pick 0, then product becomes 0.
                # However, we must be careful: the number 0 itself is not positive, but our DP counts numbers with leading zeros as well.
                # Actually, the DP counts numbers from 0 to n. But we want positive integers.
                # The number 0 has digit sum 0 and product 1 (or undefined). Our loop for s starts at 1, so 0 won't be counted.
                # But numbers with leading zeros (like 05) are interpreted as 5. The DP naturally handles this because we are building digit by digit.
                # However, we need to ensure that we don't count the number 0. Since s>=1, and 0 has sum 0, it won't be counted.
                # One issue: when we start, current_prod_mod_s should be 1 (multiplicative identity). But if the first digit is 0, then product becomes 0.
                # This is correct: 0 * d = 0.
                # But what about the number 0 itself? It has one digit 0. Sum=0, which is not in [1,81], so it won't be counted. Correct.
                total += dp(0, True, 0, 1)
            
            return total
        
        return count_up_to(r) - count_up_to(l - 1)