from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials up to 100, capping at INF to avoid overflow
        INF = 10**18
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = min(fact[i-1] * i, INF)
        
        # Helper: count ways given remaining odd/even counts and starting parity
        def count_ways(o: int, e: int, start_parity: int) -> int:
            # start_parity: 0 = even, 1 = odd
            remaining = o + e
            if remaining == 0:
                return 1
            
            # Determine how many odds and evens are needed based on start_parity
            # Positions: 0, 1, 2, ..., remaining-1
            # If start_parity == 1 (odd), odd positions: 0, 2, 4, ...
            # If start_parity == 0 (even), even positions: 0, 2, 4, ...
            # Count of start_parity positions in 'remaining' positions:
            #   ceil(remaining/2) if start_parity matches position 0
            #   floor(remaining/2) otherwise
            if start_parity == 1:
                need_odd = (remaining + 1) // 2  # ceil(remaining/2)
                need_even = remaining // 2       # floor(remaining/2)
            else:
                need_odd = remaining // 2
                need_even = (remaining + 1) // 2
            
            if o != need_odd or e != need_even:
                return 0
            
            # Number of ways: o! * e!
            result = fact[o] * fact[e]
            if result > INF:
                result = INF
            return result
        
        # Count total alternating permutations: start with odd + start with even
        total_odds = (n + 1) // 2
        total_evens = n // 2
        total = count_ways(total_odds, total_evens, 1) + count_ways(total_odds, total_evens, 0)
        if k > total:
            return []
        
        # Determine which starting parity block k falls into
        odd_start_count = count_ways(total_odds, total_evens, 1)
        if k <= odd_start_count:
            start_parity = 1
        else:
            start_parity = 0
            k -= odd_start_count
        
        # Build the permutation greedily
        used = [False] * (n + 1)
        result = []
        o_rem = total_odds
        e_rem = total_evens
        current_parity = start_parity
        
        for pos in range(n):
            # Find the smallest unused number with the required parity
            found = False
            for num in range(1, n + 1):
                if used[num]:
                    continue
                if (num % 2) != current_parity:
                    continue
                
                # Tentatively use num
                used[num] = True
                if num % 2 == 1:
                    no, ne = o_rem - 1, e_rem
                else:
                    no, ne = o_rem, e_rem - 1
                
                # Next parity
                next_parity = 1 - current_parity
                ways = count_ways(no, ne, next_parity)
                
                if k > ways:
                    k -= ways
                    used[num] = False  # backtrack
                else:
                    # This is the right choice
                    result.append(num)
                    o_rem, e_rem = no, ne
                    current_parity = next_parity
                    found = True
                    break
            
            if not found:
                # Should not happen if k is valid
                return []
        
        return result


# Test cases
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1: n=4, k=6 -> [3,4,1,2]
    print("Test 1 (n=4, k=6):", sol.permute(4, 6))
    
    # Example 2: n=3, k=2 -> [3,2,1]
    print("Test 2 (n=3, k=2):", sol.permute(3, 2))
    
    # Example 3: n=2, k=3 -> []
    print("Test 3 (n=2, k=3):", sol.permute(2, 3))
    
    # Edge case: n=1, k=1 -> [1]
    print("Test 4 (n=1, k=1):", sol.permute(1, 1))
    
    # Edge case: n=1, k=2 -> []
    print("Test 5 (n=1, k=2):", sol.permute(1, 2))
    
    # Edge case: large n, k=1 -> should give the smallest lexicographic alternating permutation
    print("Test 6 (n=10, k=1):", sol.permute(10, 1))
    
    # Edge case: k equals total count (last permutation)
    # For n=4, total = 8, so k=8 should give the last one [4,3,2,1]
    print("Test 7 (n=4, k=8):", sol.permute(4, 8))
    
    # Verify by generating all alternating permutations for n=4 and checking order
    from itertools import permutations
    def is_alternating(perm):
        for i in range(len(perm) - 1):
            if (perm[i] % 2) == (perm[i+1] % 2):
                return False
        return True
    
    all_alt = sorted([p for p in permutations(range(1, 5)) if is_alternating(p)])
    print("All alternating perms for n=4:", all_alt)
    print("k=6:", all_alt[5])  # 0-indexed
    print("k=8:", all_alt[7])
    
    # n=5 test
    all_alt5 = sorted([list(p) for p in permutations(range(1, 6)) if is_alternating(p)])
    print(f"\nAll alternating perms for n=5 ({len(all_alt5)} total):")
    for i, p in enumerate(all_alt5):
        print(f"  k={i+1}: {p}")
    # Test some specific k values
    for k_val in [1, 2, 3, 5, 10, len(all_alt5), len(all_alt5)+1]:
        result = sol.permute(5, k_val)
        if k_val <= len(all_alt5):
            expected = all_alt5[k_val-1]
            match = result == expected
            print(f"  n=5, k={k_val}: got {result}, expected {expected}, match={match}")
        else:
            print(f"  n=5, k={k_val}: got {result} (should be [])")