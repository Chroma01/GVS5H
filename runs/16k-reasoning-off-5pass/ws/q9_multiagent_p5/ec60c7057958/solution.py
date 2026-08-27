import math
from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to n
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = fact[i - 1] * i
        
        # Helper to calculate number of ways to complete the permutation
        def count_ways(rem_odd: int, rem_even: int, next_parity: int, remaining_len: int) -> int:
            # Determine required slots based on next_parity and remaining length
            # If next_parity is 1 (Odd), the sequence of length 'remaining_len' starting with Odd
            # has ceil(remaining_len/2) Odds and floor(remaining_len/2) Evens.
            if next_parity == 1: # Need Odd next
                req_odd = (remaining_len + 1) // 2
                req_even = remaining_len // 2
            else: # Need Even next
                req_odd = remaining_len // 2
                req_even = (remaining_len + 1) // 2
            
            # Check if remaining counts match required slots
            if rem_odd != req_odd or rem_even != req_even:
                return 0
            
            return fact[rem_odd] * fact[rem_even]

        # Identify available numbers
        available_odd = list(range(1, n + 1, 2))
        available_even = list(range(2, n + 1, 2))
        
        current_odd_count = len(available_odd)
        current_even_count = len(available_even)
        
        result = []
        last_parity = 0 # 0 means no previous element
        
        # We need to determine the sequence of parities first to know which numbers are valid at each step.
        # However, the problem asks for the k-th lexicographical permutation.
        # The set of valid permutations is the union of those starting with Odd and those starting with Even.
        # We can't just pick the first valid number blindly because the count of permutations starting with a specific
        # number depends on the remaining structure.
        
        # Strategy:
        # 1. Determine the total number of valid permutations. If k > total, return [].
        # 2. Iterate position by position. At each position, consider all available numbers in sorted order.
        #    Filter those that satisfy the parity constraint (different from last_parity).
        #    For each valid candidate, calculate how many valid completions exist if we pick it.
        #    If k <= count, pick it and move to next position. Else, subtract count from k and try next candidate.
        
        # To optimize, we can pre-calculate the total count to handle the k > total case early, 
        # but the loop logic naturally handles it if we ensure we don't get stuck.
        # Actually, the loop logic requires knowing the total count to verify k is valid initially? 
        # No, if k is larger than total, the loop will finish without picking a number for the last position 
        # or simply fail to find a candidate that satisfies k <= count for the first element? 
        # Wait, if k is too large, the first element loop will subtract all counts and k will remain > 0.
        # We need to check if k is within bounds before starting or handle it gracefully.
        
        # Let's calculate total valid permutations first.
        # Total = (ways starting with Odd) + (ways starting with Even)
        # Ways starting with Odd:
        #   rem_odd = current_odd_count - 1, rem_even = current_even_count
        #   next_parity = Even (since first is Odd)
        #   len = n - 1
        # Ways starting with Even:
        #   rem_odd = current_odd_count, rem_even = current_even_count - 1
        #   next_parity = Odd
        #   len = n - 1
        
        total_ways = 0
        if current_odd_count > 0:
            total_ways += count_ways(current_odd_count - 1, current_even_count, 2, n - 1)
        if current_even_count > 0:
            total_ways += count_ways(current_odd_count, current_even_count - 1, 1, n - 1)
            
        if k > total_ways:
            return []
            
        # Now construct the permutation
        for i in range(n):
            # Determine valid candidates
            # We need to check parity constraint against last_parity
            # And we need to check if picking this number allows a valid completion (which is guaranteed if k is valid and we follow logic)
            
            # Collect valid candidates in sorted order
            valid_candidates = []
            for num in sorted(available_odd + available_even):
                p = 1 if num in available_odd else 2
                if last_parity == 0 or p != last_parity:
                    valid_candidates.append(num)
            
            # If no valid candidates, something is wrong (shouldn't happen if k is valid)
            if not valid_candidates:
                return []
                
            # Iterate through valid candidates to find the one that fits k
            picked = False
            for cand in valid_candidates:
                p = 1 if cand in available_odd else 2
                
                # Calculate remaining counts if we pick 'cand'
                rem_o = current_odd_count - (1 if p == 1 else 0)
                rem_e = current_even_count - (1 if p == 2 else 0)
                rem_len = n - i - 1
                next_p = 3 - p # 3 - 1 = 2, 3 - 2 = 1
                
                cnt = count_ways(rem_o, rem_e, next_p, rem_len)
                
                if k <= cnt:
                    # Pick this candidate
                    result.append(cand)
                    if p == 1:
                        current_odd_count -= 1
                    else:
                        current_even_count -= 1
                    last_parity = p
                    picked = True
                    break
                else:
                    k -= cnt
            
            if not picked:
                # This should theoretically not happen if k <= total_ways
                return []
        
        return result

# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    n, k = 4, 6
    res = sol.permute(n, k)
    print(f"Input: n={n}, k={k}")
    print(f"Output: {res}")
    print(f"Expected: [3, 4, 1, 2]")
    print(f"Pass: {res == [3, 4, 1, 2]}\n")
    
    # Example 2
    n, k = 3, 2
    res = sol.permute(n, k)
    print(f"Input: n={n}, k={k}")
    print(f"Output: {res}")
    print(f"Expected: [3, 2, 1]")
    print(f"Pass: {res == [3, 2, 1]}\n")
    
    # Example 3
    n, k = 2, 3
    res = sol.permute(n, k)
    print(f"Input: n={n}, k={k}")
    print(f"Output: {res}")
    print(f"Expected: []")
    print(f"Pass: {res == []}\n")
    
    # Additional edge case: n=1
    n, k = 1, 1
    res = sol.permute(n, k)
    print(f"Input: n={n}, k={k}")
    print(f"Output: {res}")
    print(f"Expected: [1]")
    print(f"Pass: {res == [1]}\n")
    
    # Additional edge case: n=1, k=2 (should be empty)
    n, k = 1, 2
    res = sol.permute(n, k)
    print(f"Input: n={n}, k={k}")
    print(f"Output: {res}")
    print(f"Expected: []")
    print(f"Pass: {res == []}\n")
    
    # Additional edge case: n=5, k=1
    n, k = 5, 1
    res = sol.permute(n, k)
    print(f"Input: n={n}, k={k}")
    print(f"Output: {res}")
    print(f"Expected: [1, 2, 3, 4, 5]")
    print(f"Pass: {res == [1, 2, 3, 4, 5]}\n")