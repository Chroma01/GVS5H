class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Count odd and even numbers in [1, n]
        odd_count = (n + 1) // 2
        even_count = n // 2
        
        # Precompute DP table
        # dp[i][j][0] = number of alternating permutations using i odd and j even numbers
        #               where the next number must be even (last was odd or start with even pattern)
        # dp[i][j][1] = number of alternating permutations using i odd and j even numbers
        #               where the next number must be odd (last was even or start with odd pattern)
        # Base case: dp[0][0][0] = 1, dp[0][0][1] = 1
        dp = [[[0] * 2 for _ in range(even_count + 1)] for _ in range(odd_count + 1)]
        dp[0][0][0] = 1
        dp[0][0][1] = 1
        
        for i in range(odd_count + 1):
            for j in range(even_count + 1):
                if i == 0 and j == 0:
                    continue
                # dp[i][j][1]: next must be odd -> choose one of i odds, then next must be even
                if i > 0:
                    dp[i][j][1] = i * dp[i-1][j][0]
                # dp[i][j][0]: next must be even -> choose one of j evens, then next must be odd
                if j > 0:
                    dp[i][j][0] = j * dp[i][j-1][1]
        
        # Total alternating permutations starting with odd
        total_start_odd = odd_count * dp[odd_count-1][even_count][0] if odd_count > 0 else 0
        # Total alternating permutations starting with even
        total_start_even = even_count * dp[odd_count][even_count-1][1] if even_count > 0 else 0
        
        total = total_start_odd + total_start_even
        
        if k > total:
            return []
        
        # Determine if we start with odd or even
        start_with_odd = True
        if k > total_start_odd:
            k -= total_start_odd
            start_with_odd = False
        
        # Available numbers
        odds = [x for x in range(1, n+1) if x % 2 == 1]
        evens = [x for x in range(1, n+1) if x % 2 == 0]
        
        result = []
        last_parity = -1  # -1 means not set yet
        
        # We'll maintain counts of remaining odds and evens
        rem_odd = odd_count
        rem_even = even_count
        
        for pos in range(n):
            # Determine what parity we need next
            if pos == 0:
                # Already decided by start_with_odd
                need_odd = start_with_odd
            else:
                # Must alternate
                need_odd = (last_parity == 0)  # if last was even (0), next must be odd (1)
            
            # Find the candidate number
            if need_odd:
                # Try each available odd number in increasing order
                found = False
                for idx, num in enumerate(odds):
                    # Number of permutations if we pick this odd number
                    # After picking, rem_odd becomes rem_odd - 1, rem_even stays same
                    # Next must be even, so we use dp[rem_odd-1][rem_even][0]
                    count = dp[rem_odd-1][rem_even][0] if rem_odd > 0 else 0
                    
                    if k <= count:
                        result.append(num)
                        odds.pop(idx)
                        rem_odd -= 1
                        last_parity = 1  # 1 for odd
                        found = True
                        break
                    else:
                        k -= count
                if not found:
                    return []  # Should not happen if k is valid
            else:
                # Try each available even number in increasing order
                found = False
                for idx, num in enumerate(evens):
                    # Number of permutations if we pick this even number
                    # After picking, rem_even becomes rem_even - 1, rem_odd stays same
                    # Next must be odd, so we use dp[rem_odd][rem_even-1][1]
                    count = dp[rem_odd][rem_even-1][1] if rem_even > 0 else 0
                    
                    if k <= count:
                        result.append(num)
                        evens.pop(idx)
                        rem_even -= 1
                        last_parity = 0  # 0 for even
                        found = True
                        break
                    else:
                        k -= count
                if not found:
                    return []  # Should not happen if k is valid
        
        return result