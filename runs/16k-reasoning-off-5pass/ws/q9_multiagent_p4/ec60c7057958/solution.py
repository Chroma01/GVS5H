from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute DP tables
        # dp_odd[L][o] = ways to arrange L items with o odds (L-o evens) starting with Odd
        # dp_even[L][o] = ways to arrange L items with o odds (L-o evens) starting with Even
        
        # Initialize DP tables
        # Dimensions: L from 0 to n, o from 0 to n
        dp_odd = [[0] * (n + 1) for _ in range(n + 1)]
        dp_even = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Base case: 0 items left, 0 odds left -> 1 way (empty sequence)
        dp_odd[0][0] = 1
        dp_even[0][0] = 1
        
        # Fill DP tables
        for L in range(1, n + 1):
            for o in range(L + 1):  # o can be at most L
                # Calculate dp_odd[L][o]
                # To start with Odd, we pick one of 'o' odds.
                # Remaining: L-1 items, o-1 odds, must start with Even.
                if o > 0:
                    dp_odd[L][o] = o * dp_even[L - 1][o - 1]
                
                # Calculate dp_even[L][o]
                # To start with Even, we pick one of 'L-o' evens.
                # Remaining: L-1 items, o odds, must start with Odd.
                if (L - o) > 0:
                    dp_even[L][o] = (L - o) * dp_odd[L - 1][o]
        
        # Calculate total valid permutations
        # Total = (ways starting with Odd) + (ways starting with Even)
        # We have n numbers: ceil(n/2) odds, floor(n/2) evens.
        total_odds = (n + 1) // 2
        total_evens = n // 2
        
        # Ways starting with Odd: pick one of total_odds, then arrange n-1 with total_odds-1 odds starting Even
        ways_start_odd = 0
        if total_odds > 0:
            ways_start_odd = total_odds * dp_even[n - 1][total_odds - 1]
            
        # Ways starting with Even: pick one of total_evens, then arrange n-1 with total_odds odds starting Odd
        ways_start_even = 0
        if total_evens > 0:
            ways_start_even = total_evens * dp_odd[n - 1][total_odds]
            
        total_permutations = ways_start_odd + ways_start_even
        
        if k > total_permutations:
            return []
        
        result = []
        used = [False] * (n + 1)
        last_parity = -1  # -1: none, 0: even, 1: odd
        
        # Helper to get parity: 1 for odd, 0 for even
        def get_parity(x):
            return x % 2
        
        for i in range(1, n + 1):
            # Determine required parity for current position
            # If last_parity is -1, any parity is allowed (handled by loop check)
            # If last_parity is set, next must be different
            if last_parity != -1:
                required_parity = 1 - last_parity
            else:
                required_parity = -1 # No constraint
            
            # Iterate through available numbers in increasing order (lexicographical)
            for x in range(1, n + 1):
                if used[x]:
                    continue
                
                current_parity = get_parity(x)
                
                # Check if parity matches constraint
                if last_parity != -1 and current_parity == last_parity:
                    continue
                
                # Calculate number of ways if we pick x
                remaining_len = n - i
                remaining_odds = total_odds - (1 if current_parity == 1 else 0)
                
                if remaining_len == 0:
                    count = 1
                else:
                    # The next element (if any) must have parity opposite to current_parity
                    next_required_parity = 1 - current_parity
                    if next_required_parity == 1: # Next must be Odd
                        count = dp_odd[remaining_len][remaining_odds]
                    else: # Next must be Even
                        count = dp_even[remaining_len][remaining_odds]
                
                if k <= count:
                    # Pick this number
                    result.append(x)
                    used[x] = True
                    last_parity = current_parity
                    break
                else:
                    k -= count
        
        return result