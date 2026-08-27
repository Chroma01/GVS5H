class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Count odd and even numbers in [1, n]
        o = (n + 1) // 2  # number of odds
        e = n // 2          # number of evens
        
        # dp[i][j][req] = number of ways to arrange i odds and j evens
        # such that the next number to be placed has parity 'req'
        # req = 0 means next must be even
        # req = 1 means next must be odd
        # Dimensions: (o+1) x (e+1) x 2
        dp = [[[0] * 2 for _ in range(e + 1)] for _ in range(o + 1)]
        
        # Base case: 0 odds and 0 evens left, one way (empty sequence)
        dp[0][0][0] = 1
        dp[0][0][1] = 1
        
        # Fill DP table
        for i in range(o + 1):
            for j in range(e + 1):
                # If we need to place an even number next (req=0)
                # We must have at least one even number available
                if j > 0:
                    # After placing an even, next required is odd (1)
                    dp[i][j][0] += dp[i][j - 1][1]
                # If we need to place an odd number next (req=1)
                # We must have at least one odd number available
                if i > 0:
                    # After placing an odd, next required is even (0)
                    dp[i][j][1] += dp[i - 1][j][0]
        
        # Total alternating permutations
        total = dp[o][e][0] + dp[o][e][1]
        if k > total:
            return []
        
        # Available numbers
        odds = [x for x in range(1, n + 1) if x % 2 == 1]
        evens = [x for x in range(1, n + 1) if x % 2 == 0]
        
        result = []
        # Remaining counts
        rem_o = o
        rem_e = e
        
        # For the first position, there is no "last parity", so we consider both starts
        # But actually, we can think of it as: we need to choose the first number.
        # If we choose an even number, then the remaining problem is: arrange rem_o odds and rem_e-1 evens, with next required parity = odd (1)
        # If we choose an odd number, then the remaining problem is: arrange rem_o-1 odds and rem_e evens, with next required parity = even (0)
        
        # We'll iterate position by position
        for pos in range(n):
            # Determine which numbers are still available
            # We'll maintain lists of available odds and evens
            # But to efficiently find the k-th, we iterate through candidates in order
            
            # Combined sorted list of available numbers
            # Instead of maintaining separate lists and merging, we can just iterate 1..n and check if used
            # But n is up to 100, so O(n^2) is acceptable.
            
            # Actually, we can maintain two sorted lists: available_odds and available_evens
            # But for simplicity and correctness, let's use a set of used numbers and iterate 1..n
            
            # However, to make it efficient, we'll keep available_odds and available_evens as sorted lists
            # Initially:
            if pos == 0:
                available_odds = [x for x in range(1, n + 1) if x % 2 == 1]
                available_evens = [x for x in range(1, n + 1) if x % 2 == 0]
            else:
                # We'll update these lists as we go? Actually, better to just filter from original or maintain.
                # Let's maintain them.
                pass
            
            # Instead, let's just use the lists and remove elements as we pick them.
            # But removing from list is O(n). With n=100, it's fine.
            
            # Actually, we haven't defined available_odds and available_evens for pos>0 yet.
            # Let's redefine: we'll keep two lists that we modify.
            if pos == 0:
                available_odds = [x for x in range(1, n + 1) if x % 2 == 1]
                available_evens = [x for x in range(1, n + 1) if x % 2 == 0]
            
            # Get all available numbers in sorted order
            all_available = sorted(available_odds + available_evens)
            
            found = False
            for num in all_available:
                if num % 2 == 1:
                    # num is odd
                    # If this is the first position, the count of permutations starting with this odd
                    # is: dp[rem_o - 1][rem_e][0]  (because after placing odd, next must be even -> req=0)
                    # If not first position, we need to know the last parity. But we don't store it explicitly.
                    # Actually, the DP state depends on the required next parity, which is determined by the last placed number's parity.
                    # For the first position, we don't have a last parity. So we handle first position separately in logic below.
                    
                    # For positions > 0, the required next parity is determined by the last placed number.
                    # But we are constructing sequentially. We need to know what parity is required next.
                    # Let's track the required next parity.
                    pass
                else:
                    pass
            
            # Better approach: track the required next parity.
            # For the first position, we try both even and odd candidates, but we need to know which ones are available.
            # Actually, we can unify: 
            # Let req be the required parity for the current position.
            # For pos=0, there is no requirement, so we try all available numbers. But the count for a candidate depends on what parity it is.
            # Specifically:
            #   If candidate is even: count = dp[rem_o][rem_e - 1][1]  (after placing even, next must be odd)
            #   If candidate is odd: count = dp[rem_o - 1][rem_e][0]   (after placing odd, next must be even)
            # For pos>0, the required parity is fixed by the previous choice.
            #   If last was even, next must be odd. So only odd candidates are considered.
            #   If last was odd, next must be even. So only even candidates are considered.
            
            # So, we need to track the required parity for the current position.
            # Let's define: req_next = 0 if next must be even, 1 if next must be odd.
            # For pos=0, we don't have a req_next. We can set req_next = -1 to indicate "any".
            
            # Actually, we can handle pos=0 by considering both parities, but then for pos>0, req_next is determined.
            
            # Let's restart the loop logic with req_next tracking.
            pass
        
        # Redo the construction with req_next
        available_odds = [x for x in range(1, n + 1) if x % 2 == 1]
        available_evens = [x for x in range(1, n + 1) if x % 2 == 0]
        
        result = []
        rem_o = o
        rem_e = e
        req_next = -1  # -1 means no requirement (first position)
        
        for pos in range(n):
            # Determine which candidates to consider
            if req_next == -1:
                # Consider all available numbers
                candidates = sorted(available_odds + available_evens)
            elif req_next == 0:
                # Next must be even
                candidates = available_evens
            else: # req_next == 1
                # Next must be odd
                candidates = available_odds
            
            found = False
            for num in candidates:
                if num % 2 == 1:
                    # num is odd
                    if req_next == -1:
                        # First position, placing odd
                        # Count = dp[rem_o - 1][rem_e][0]
                        cnt = dp[rem_o - 1][rem_e][0] if rem_o > 0 else 0
                    else:
                        # Not first position, and req_next must be 1 (since num is odd)
                        # After placing odd, next required is even (0)
                        cnt = dp[rem_o - 1][rem_e][0] if rem_o > 0 else 0
                else:
                    # num is even
                    if req_next == -1:
                        # First position, placing even
                        # Count = dp[rem_o][rem_e - 1][1]
                        cnt = dp[rem_o][rem_e - 1][1] if rem_e > 0 else 0
                    else:
                        # Not first position, and req_next must be 0 (since num is even)
                        # After placing even, next required is odd (1)
                        cnt = dp[rem_o][rem_e - 1][1] if rem_e > 0 else 0
                
                if k <= cnt:
                    # Place this number
                    result.append(num)
                    if num % 2 == 1:
                        rem_o -= 1
                        req_next = 0  # next must be even
                    else:
                        rem_e -= 1
                        req_next = 1  # next must be odd
                    
                    # Remove num from available lists
                    if num in available_odds:
                        available_odds.remove(num)
                    else:
                        available_evens.remove(num)
                    
                    found = True
                    break
                else:
                    k -= cnt
            
            if not found:
                return []
        
        return result