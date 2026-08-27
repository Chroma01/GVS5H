class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials, capped at a value larger than max k (10^15)
        # We cap at 10^15 + 7 to avoid huge number arithmetic, but Python handles big ints fine.
        # Given n <= 100, 100! is huge, but we only care if count >= k.
        INF = 10**16
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(fact[i-1] * i, INF)
            
        # Separate odd and even numbers
        odds = [x for x in range(1, n + 1) if x % 2 == 1]
        evens = [x for x in range(1, n + 1) if x % 2 == 0]
        
        # Count initial available odds and evens
        rem_odd = len(odds)
        rem_even = len(evens)
        
        used = [False] * (n + 1)
        result = []
        
        # Helper to count required odds/evens for remaining positions
        # Given the last chosen number's parity (last_parity), 
        # count how many odd and even positions are needed for positions i+1 to n-1.
        def count_required(last_parity, positions_left):
            # positions_left is the number of positions to fill after the current one
            # The next position must have parity different from last_parity
            req_odd = 0
            req_even = 0
            # The parity sequence for the remaining positions is fixed and alternating
            # Start with parity different from last_parity
            curr_parity = 1 - last_parity # 0 for even, 1 for odd
            
            for _ in range(positions_left):
                if curr_parity == 1:
                    req_odd += 1
                else:
                    req_even += 1
                curr_parity = 1 - curr_parity
            return req_odd, req_even

        for i in range(n):
            # Determine candidates for position i
            if i == 0:
                # No previous constraint, try all available numbers in increasing order
                candidates = []
                for x in range(1, n + 1):
                    if not used[x]:
                        candidates.append(x)
            else:
                # Must have different parity from previous
                prev_parity = result[-1] % 2
                candidates = []
                for x in range(1, n + 1):
                    if not used[x] and (x % 2 != prev_parity):
                        candidates.append(x)
            
            chosen = False
            for c in candidates:
                # Calculate number of valid completions if we pick c
                # Determine remaining odds and evens after picking c
                r_odd = rem_odd
                r_even = rem_even
                if c % 2 == 1:
                    r_odd -= 1
                else:
                    r_even -= 1
                
                positions_left = n - 1 - i
                if positions_left == 0:
                    count = 1
                else:
                    # Count required odds and evens for the remaining positions
                    # The next position (i+1) must have parity different from c
                    req_odd, req_even = count_required(c % 2, positions_left)
                    
                    if req_odd == r_odd and req_even == r_even:
                        count = fact[r_odd] * fact[r_even]
                    else:
                        count = 0
                
                if k <= count:
                    # Pick this candidate
                    result.append(c)
                    used[c] = True
                    if c % 2 == 1:
                        rem_odd -= 1
                    else:
                        rem_even -= 1
                    chosen = True
                    break
                else:
                    k -= count
            
            if not chosen:
                return []
                
        return result