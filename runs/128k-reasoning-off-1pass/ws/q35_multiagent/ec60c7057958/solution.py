class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Count of odd and even numbers in 1..n
        num_odds = (n + 1) // 2
        num_evens = n // 2
        
        # dp[o][e][0] = number of alternating perms with o odds, e evens, starting with even
        # dp[o][e][1] = number of alternating perms with o odds, e evens, starting with odd
        # We'll use a 2D array for each start parity, or a 3D array.
        # Dimensions: (num_odds+1) x (num_evens+1) x 2
        dp = [[[0] * 2 for _ in range(num_evens + 1)] for _ in range(num_odds + 1)]
        
        # Base case: 0 odds, 0 evens -> 1 way (empty permutation)
        dp[0][0][0] = 1
        dp[0][0][1] = 1
        
        # Fill DP table
        for o in range(num_odds + 1):
            for e in range(num_evens + 1):
                if o == 0 and e == 0:
                    continue
                # If starting with odd: we pick one odd, then remaining must start with even
                if o > 0:
                    dp[o][e][1] = o * dp[o-1][e][0]
                # If starting with even: we pick one even, then remaining must start with odd
                if e > 0:
                    dp[o][e][0] = e * dp[o][e-1][1]
        
        # Check if k is valid
        total = 0
        # Total alternating permutations = sum over all valid starts
        # Actually, total = dp[num_odds][num_evens][0] + dp[num_odds][num_evens][1]
        # But note: dp[num_odds][num_evens][0] counts perms starting with even
        # dp[num_odds][num_evens][1] counts perms starting with odd
        total = dp[num_odds][num_evens][0] + dp[num_odds][num_evens][1]
        
        if k > total:
            return []
        
        # Available numbers
        odds = list(range(1, n + 1, 2))  # [1, 3, 5, ...]
        evens = list(range(2, n + 1, 2))  # [2, 4, 6, ...]
        
        result = []
        remaining_odds = num_odds
        remaining_evens = num_evens
        
        for i in range(n):
            # Determine which list to try: odds or evens
            # For position 0, we can try any available number.
            # For position > 0, the parity is determined by the previous element.
            if i == 0:
                # Try all available numbers in increasing order
                candidates = []
                # We need to merge odds and evens in sorted order
                oi, ei = 0, 0
                while oi < len(odds) and ei < len(evens):
                    if odds[oi] < evens[ei]:
                        candidates.append(odds[oi])
                        oi += 1
                    else:
                        candidates.append(evens[ei])
                        ei += 1
                while oi < len(odds):
                    candidates.append(odds[oi])
                    oi += 1
                while ei < len(evens):
                    candidates.append(evens[ei])
                    ei += 1
            else:
                # Parity must be different from last element
                last_parity = result[-1] % 2
                if last_parity == 1:  # last was odd, next must be even
                    candidates = evens
                else:  # last was even, next must be odd
                    candidates = odds
            
            found = False
            for cand in candidates:
                # Calculate how many valid permutations start with cand
                # After picking cand, remaining odds and evens:
                if cand % 2 == 1:  # odd
                    rem_o = remaining_odds - 1
                    rem_e = remaining_evens
                    next_start_parity = 0  # next must be even
                else:  # even
                    rem_o = remaining_odds
                    rem_e = remaining_evens - 1
                    next_start_parity = 1  # next must be odd
                
                # Count = dp[rem_o][rem_e][next_start_parity]
                count = dp[rem_o][rem_e][next_start_parity]
                
                if k <= count:
                    # Pick this candidate
                    result.append(cand)
                    if cand % 2 == 1:
                        odds.remove(cand)
                        remaining_odds -= 1
                    else:
                        evens.remove(cand)
                        remaining_evens -= 1
                    found = True
                    break
                else:
                    k -= count
            
            if not found:
                # Should not happen if k is valid
                return []
        
        return result