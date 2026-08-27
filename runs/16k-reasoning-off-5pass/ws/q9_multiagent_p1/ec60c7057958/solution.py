import math
from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials for P(n, k) calculation
        # P(n, k) = n! / (n-k)!
        # Since n <= 100, we can precompute factorials up to 100
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = fact[i - 1] * i
            
        def P(n_val: int, k_val: int) -> int:
            if k_val < 0 or k_val > n_val:
                return 0
            return fact[n_val] // fact[n_val - k_val]

        # Count available odds and evens in 1..n
        cnt_odd = (n + 1) // 2
        cnt_even = n // 2
        
        # Calculate total valid permutations
        # Case 1: Start with Odd
        # Requires ceil(n/2) odds and floor(n/2) evens
        req_odd_start_odd = (n + 1) // 2
        req_even_start_odd = n // 2
        ways_start_odd = P(cnt_odd, req_odd_start_odd) * P(cnt_even, req_even_start_odd)
        
        # Case 2: Start with Even
        # Requires floor(n/2) odds and ceil(n/2) evens
        req_odd_start_even = n // 2
        req_even_start_even = (n + 1) // 2
        ways_start_even = P(cnt_odd, req_odd_start_even) * P(cnt_even, req_even_start_even)
        
        total_ways = ways_start_odd + ways_start_even
        
        if k > total_ways:
            return []
        
        result = []
        prev_parity = -1  # -1 for none, 0 for even, 1 for odd
        used = [False] * (n + 1)
        
        for pos in range(n):
            # Determine required parity for this position based on previous
            if prev_parity != -1:
                required_parity = 1 - prev_parity
            else:
                required_parity = -1  # No constraint for the first element
            
            # Iterate through available numbers in increasing order
            for x in range(1, n + 1):
                if used[x]:
                    continue
                
                # Check parity constraint
                if prev_parity != -1:
                    if (x % 2) == prev_parity:
                        continue  # Same parity, invalid
                
                # Calculate ways if we pick x
                rem_len = n - 1 - pos
                new_cnt_odd = cnt_odd - (1 if (x % 2 == 1) else 0)
                new_cnt_even = cnt_even - (1 if (x % 2 == 0) else 0)
                
                # Determine required counts for the remaining positions
                # The sequence of parities for the remaining positions is fixed once we pick x.
                # If we picked x (parity p), the next must be 1-p, then p, etc.
                next_parity = 1 - (x % 2)  # 1 for odd, 0 for even
                
                # Calculate how many odd/even slots are needed in the remaining 'rem_len' positions
                # Pattern starts with 'next_parity'
                if next_parity == 1:  # Next is Odd
                    req_odd_rem = (rem_len + 1) // 2
                    req_even_rem = rem_len // 2
                else:  # Next is Even
                    req_odd_rem = rem_len // 2
                    req_even_rem = (rem_len + 1) // 2
                
                ways = P(new_cnt_odd, req_odd_rem) * P(new_cnt_even, req_even_rem)
                
                if k <= ways:
                    # Pick x
                    result.append(x)
                    used[x] = True
                    prev_parity = x % 2
                    cnt_odd = new_cnt_odd
                    cnt_even = new_cnt_even
                    break  # Move to next position
                else:
                    k -= ways
        
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
    
    # Edge case: n=1, k=1
    res4 = sol.permute(1, 1)
    print(f"n=1, k=1 -> {res4}")
    assert res4 == [1], f"Expected [1], got {res4}"
    
    # Edge case: n=1, k=2 (should be empty)
    res5 = sol.permute(1, 2)
    print(f"n=1, k=2 -> {res5}")
    assert res5 == [], f"Expected [], got {res5}"
    
    # Additional check: n=4, k=1 (first permutation)
    res6 = sol.permute(4, 1)
    print(f"n=4, k=1 -> {res6}")
    assert res6 == [1, 2, 3, 4], f"Expected [1, 2, 3, 4], got {res6}"
    
    # Additional check: n=4, k=8 (last permutation)
    res7 = sol.permute(4, 8)
    print(f"n=4, k=8 -> {res7}")
    assert res7 == [4, 3, 2, 1], f"Expected [4, 3, 2, 1], got {res7}"
    
    print("All tests passed.")