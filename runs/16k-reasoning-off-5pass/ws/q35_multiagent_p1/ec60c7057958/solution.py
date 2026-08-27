class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Count odd and even numbers in [1, n]
        odd_count = (n + 1) // 2
        even_count = n // 2
        
        # Precompute factorials up to n
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = fact[i - 1] * i
        
        # Calculate number of valid permutations for each pattern
        # Pattern A: positions 0,2,4... are Odd; positions 1,3,5... are Even
        # Requires ceil(n/2) odds and floor(n/2) evens
        need_odd_A = (n + 1) // 2
        need_even_A = n // 2
        
        countA = 0
        if odd_count >= need_odd_A and even_count >= need_even_A:
            countA = fact[need_odd_A] * fact[need_even_A]
        
        # Pattern B: positions 0,2,4... are Even; positions 1,3,5... are Odd
        # Requires ceil(n/2) evens and floor(n/2) odds
        need_even_B = (n + 1) // 2
        need_odd_B = n // 2
        
        countB = 0
        if even_count >= need_even_B and odd_count >= need_odd_B:
            countB = fact[need_even_B] * fact[need_odd_B]
        
        total = countA + countB
        if k > total:
            return []
        
        # Determine which pattern to use
        if k <= countA:
            # Use Pattern A: even indices get odd numbers, odd indices get even numbers
            # For position i, required parity: i % 2 == 0 -> odd, i % 2 == 1 -> even
            use_pattern_A = True
        else:
            # Use Pattern B: even indices get even numbers, odd indices get odd numbers
            # For position i, required parity: i % 2 == 0 -> even, i % 2 == 1 -> odd
            use_pattern_A = False
            k -= countA
        
        # Build the permutation
        result = []
        # Available numbers: all numbers from 1 to n
        available = list(range(1, n + 1))
        
        # Track remaining counts of odd and even numbers
        rem_odd = odd_count
        rem_even = even_count
        
        for i in range(n):
            # Determine required parity for position i
            if use_pattern_A:
                req_parity = 1 if i % 2 == 0 else 0  # 1 for odd, 0 for even
            else:
                req_parity = 0 if i % 2 == 0 else 1  # 0 for even, 1 for odd
            
            # Iterate through available numbers in increasing order
            for idx, num in enumerate(available):
                # Check if num has the required parity
                num_parity = num % 2
                if num_parity != req_parity:
                    continue
                
                # Calculate number of valid completions if we pick this number
                # After picking, remaining odds and evens are:
                if num_parity == 1:  # odd
                    new_rem_odd = rem_odd - 1
                    new_rem_even = rem_even
                else:  # even
                    new_rem_odd = rem_odd
                    new_rem_even = rem_even - 1
                
                # The number of ways to fill the remaining positions is:
                # new_rem_odd! * new_rem_even!
                # Because the pattern is fixed, and the remaining positions will require
                # exactly new_rem_odd odds and new_rem_even evens in their respective slots.
                count = fact[new_rem_odd] * fact[new_rem_even]
                
                if k <= count:
                    # Pick this number
                    result.append(num)
                    available.pop(idx)
                    rem_odd = new_rem_odd
                    rem_even = new_rem_even
                    break
                else:
                    k -= count
        
        return result