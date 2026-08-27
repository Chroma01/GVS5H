from functools import lru_cache
from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Cap value to avoid overflow and unnecessary large number calculations.
        # k <= 10^15, so 10^18 is sufficient to treat as infinity.
        INF = 10**18
        
        @lru_cache(maxsize=None)
        def count_perms(length: int, odds: int, evens: int, next_parity: int) -> int:
            """
            Returns the number of valid alternating permutations of length 'length'
            using 'odds' odd numbers and 'evens' even numbers, where the next element
            must have parity 'next_parity' (0 for Odd, 1 for Even).
            """
            if length == 0:
                return 1
            
            if odds < 0 or evens < 0:
                return 0
            
            if next_parity == 0 and odds == 0:
                return 0
            if next_parity == 1 and evens == 0:
                return 0
            
            if length > odds + evens:
                return 0
            
            res = 0
            if next_parity == 0: # Need Odd
                # We have 'odds' choices for the current position.
                # The rest of the permutation must start with Even.
                ways = odds * count_perms(length - 1, odds - 1, evens, 1)
            else: # Need Even
                # We have 'evens' choices for the current position.
                # The rest of the permutation must start with Odd.
                ways = evens * count_perms(length - 1, odds, evens - 1, 0)
            
            # Cap the result to prevent overflow and speed up comparisons
            if ways > INF:
                ways = INF + 1
            return ways

        # Initial counts of odd and even numbers in [1, n]
        odds_count = (n + 1) // 2
        evens_count = n // 2
        
        # Calculate total valid permutations
        # Sum of those starting with Odd and those starting with Even
        total = count_perms(n, odds_count, evens_count, 0) + count_perms(n, odds_count, evens_count, 1)
        
        if k > total:
            return []
        
        result = []
        curr_odds = odds_count
        curr_evens = evens_count
        last_parity = -1 # -1 indicates no previous element
        
        for i in range(n):
            remaining_len = n - i
            
            # Determine allowed parity for the current position
            if last_parity == -1:
                allowed_parity = None # Both allowed
            else:
                allowed_parity = 1 - last_parity # Must be different
            
            # Collect available candidates in increasing order
            candidates = []
            for x in range(1, n + 1):
                # Check if x is already used (in result)
                if x in result:
                    continue
                
                p = x % 2
                # Check parity constraint
                if allowed_parity is None or p == allowed_parity:
                    candidates.append(x)
            
            # Iterate through candidates to find the correct one
            for x in candidates:
                p = x % 2
                
                # Calculate number of completions if we pick x
                if p == 0: # Odd
                    # Remaining: odds-1, evens, next_parity=1 (Even)
                    cnt = count_perms(remaining_len - 1, curr_odds - 1, curr_evens, 1)
                else: # Even
                    # Remaining: odds, evens-1, next_parity=0 (Odd)
                    cnt = count_perms(remaining_len - 1, curr_odds, curr_evens - 1, 0)
                
                if k <= cnt:
                    # Found the correct number
                    result.append(x)
                    if p == 0:
                        curr_odds -= 1
                    else:
                        curr_evens -= 1
                    last_parity = p
                    break
                else:
                    # Skip this number and adjust k
                    k -= cnt
        
        return result

# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    res1 = sol.permute(4, 6)
    print(f"n=4, k=6 -> {res1}")
    assert res1 == [3, 4, 1, 2], f"Expected [3, 4, 1, 2], got {res1}"
    
    # Example 2
    res2 = sol.permute(3, 2)
    print(f"n=3, k=2 -> {res2}")
    assert res2 == [3, 2, 1], f"Expected [3, 2, 1], got {res2}"
    
    # Example 3
    res3 = sol.permute(2, 3)
    print(f"n=2, k=3 -> {res3}")
    assert res3 == [], f"Expected [], got {res3}"
    
    # Edge case: n=1
    res4 = sol.permute(1, 1)
    print(f"n=1, k=1 -> {res4}")
    assert res4 == [1], f"Expected [1], got {res4}"
    
    # Edge case: n=1, k=2 (should be empty)
    res5 = sol.permute(1, 2)
    print(f"n=1, k=2 -> {res5}")
    assert res5 == [], f"Expected [], got {res5}"
    
    # Large k test (n=4, k=9 should be empty as total is 8)
    res6 = sol.permute(4, 9)
    print(f"n=4, k=9 -> {res6}")
    assert res6 == [], f"Expected [], got {res6}"
    
    # Large n test (n=10, k=1)
    res7 = sol.permute(10, 1)
    print(f"n=10, k=1 -> {res7}")
    # First permutation should be 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    assert res7 == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], f"Expected [1..10], got {res7}"
    
    print("All tests passed.")