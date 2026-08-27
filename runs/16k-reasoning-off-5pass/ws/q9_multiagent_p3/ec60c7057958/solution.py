from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to n
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = fact[i - 1] * i
        
        def P(n_val: int, k_val: int) -> int:
            if k_val < 0 or k_val > n_val:
                return 0
            return fact[n_val] // fact[n_val - k_val]
        
        # Count available odds and evens in 1..n
        num_odds = (n + 1) // 2
        num_evens = n // 2
        
        # Determine required counts for two patterns
        # Pattern A: Starts with Odd -> O, E, O, E...
        # Needs ceil(n/2) odds, floor(n/2) evens
        req_o_a = (n + 1) // 2
        req_e_a = n // 2
        
        # Pattern B: Starts with Even -> E, O, E, O...
        # Needs floor(n/2) odds, ceil(n/2) evens
        req_o_b = n // 2
        req_e_b = (n + 1) // 2
        
        # Calculate total valid permutations for each pattern
        count_a = 0
        if num_odds >= req_o_a and num_evens >= req_e_a:
            count_a = P(num_odds, req_o_a) * P(num_evens, req_e_a)
            
        count_b = 0
        if num_odds >= req_o_b and num_evens >= req_e_b:
            count_b = P(num_odds, req_o_b) * P(num_evens, req_e_b)
            
        total_perms = count_a + count_b
        if k > total_perms:
            return []
        
        result = []
        used = [False] * (n + 1)
        used_o = 0
        used_e = 0
        
        # Determine the first element by iterating candidates in lexicographical order
        # Candidates for position 0
        candidates_0 = []
        for x in range(1, n + 1):
            if not used[x]:
                candidates_0.append(x)
        
        first_elem = -1
        for x in candidates_0:
            is_odd = (x % 2 != 0)
            
            # Calculate ways if we pick x
            if is_odd:
                # Pattern A (Starts Odd)
                needed_o = req_o_a - 1
                needed_e = req_e_a
                avail_o = num_odds - 1
                avail_e = num_evens
                
                if avail_o >= needed_o and avail_e >= needed_e:
                    ways = P(avail_o, needed_o) * P(avail_e, needed_e)
                else:
                    ways = 0
            else:
                # Pattern B (Starts Even)
                needed_o = req_o_b
                needed_e = req_e_b - 1
                avail_o = num_odds
                avail_e = num_evens - 1
                
                if avail_o >= needed_o and avail_e >= needed_e:
                    ways = P(avail_o, needed_o) * P(avail_e, needed_e)
                else:
                    ways = 0
            
            if k <= ways:
                first_elem = x
                break
            else:
                k -= ways
        
        if first_elem == -1:
            return []
        
        result.append(first_elem)
        used[first_elem] = True
        if first_elem % 2 != 0:
            used_o += 1
            start_odd = True
        else:
            used_e += 1
            start_odd = False
            
        # Fill the rest of the positions
        for i in range(1, n):
            # Determine required parity for position i based on start_odd
            if start_odd:
                current_parity = 'odd' if i % 2 == 0 else 'even'
            else:
                current_parity = 'even' if i % 2 == 0 else 'odd'
            
            # Collect candidates of the required parity
            candidates = []
            if current_parity == 'odd':
                for x in range(1, n + 1, 2):
                    if not used[x]:
                        candidates.append(x)
            else:
                for x in range(2, n + 1, 2):
                    if not used[x]:
                        candidates.append(x)
            
            # Total requirements for the FULL sequence based on start_odd
            if start_odd:
                total_req_o = req_o_a
                total_req_e = req_e_a
            else:
                total_req_o = req_o_b
                total_req_e = req_e_b
            
            for x in candidates:
                # Calculate remaining needs if we pick x
                # We need to fill positions i+1 to n-1 (length n - 1 - i)
                # The parity of position i+1 is fixed by start_odd and i
                
                # Total odds needed = total_req_o.
                # Odds used so far (including x) = used_o + (1 if x is odd else 0)
                # Remaining odds to fill = total_req_o - (odds used so far)
                
                rem_o_needed = total_req_o - used_o - (1 if x % 2 != 0 else 0)
                rem_e_needed = total_req_e - used_e - (1 if x % 2 == 0 else 0)
                
                available_o = num_odds - used_o - (1 if x % 2 != 0 else 0)
                available_e = num_evens - used_e - (1 if x % 2 == 0 else 0)
                
                # Check if valid
                if available_o >= rem_o_needed and available_e >= rem_e_needed:
                    ways = P(available_o, rem_o_needed) * P(available_e, rem_e_needed)
                else:
                    ways = 0
                
                if k <= ways:
                    result.append(x)
                    used[x] = True
                    if x % 2 != 0:
                        used_o += 1
                    else:
                        used_e += 1
                    break
                else:
                    k -= ways
                    
        return result