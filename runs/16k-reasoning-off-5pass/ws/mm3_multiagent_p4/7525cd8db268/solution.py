from typing import List
from collections import Counter

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Build ends[b] = list of a's where pair is (a,b) with a < b
        ends = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            lo, hi = (a, b) if a < b else (b, a)
            ends[hi].append(lo)
        
        # gain[lo] = total extra subarrays if we remove a pair with this lo value
        gain = [0] * (n + 1)
        
        base = 0
        mx1 = 0   # current maximum blocker value
        mx2 = 0   # second maximum blocker value
        cnt_mx1 = 0  # how many active pairs have blocker == mx1
        
        for i in range(1, n + 1):
            # Add all new blockers whose right endpoint is i
            for lo in ends[i]:
                if lo > mx1:
                    mx2 = mx1
                    mx1 = lo
                    cnt_mx1 = 1
                elif lo == mx1:
                    cnt_mx1 += 1
                elif lo > mx2:
                    mx2 = lo
            
            # Subarrays ending at i that are valid with all pairs
            base += i - mx1
            
            # If mx1 is unique, removing that pair lowers blocker to mx2
            if cnt_mx1 == 1:
                gain[mx1] += mx1 - mx2
        
        return base + max(gain)


# ----------------------------------------------------------------------
# Test harness
# ----------------------------------------------------------------------
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    n1 = 4
    pairs1 = [[2, 3], [1, 4]]
    print("Example 1:", sol.maxSubarrays(n1, pairs1))  # Expected: 9
    
    # Example 2
    n2 = 5
    pairs2 = [[1, 2], [2, 5], [3, 5]]
    print("Example 2:", sol.maxSubarrays(n2, pairs2))  # Expected: 12
    
    # Edge case: n=2, one pair
    n3 = 2
    pairs3 = [[1, 2]]
    print("n=2, one pair:", sol.maxSubarrays(n3, pairs3))
    # Without removal, only subarrays not containing both 1 and 2: [1], [2] -> 2
    # With removal of the only pair, all 3 subarrays are valid -> max is 3
    # Expected: 3
    
    # Edge case: all pairs identical
    n4 = 3
    pairs4 = [[1, 2], [1, 2], [1, 2]]
    print("Three identical pairs:", sol.maxSubarrays(n4, pairs4))
    # Removing one doesn't help (two remain blocking), so answer = 2
    # Subarrays avoiding [1,2]: [1], [2], [3] -> wait, [1,2] is the only bad one
    # [1], [2], [3], [1,2,3] all avoid having both 1 and 2? 
    # [1,2,3] contains both 1 and 2, so it's bad.
    # Valid: [1], [2], [3], [1,2,3]? No [1,2,3] contains both.
    # Valid: [1], [2], [3], [2,3]? [2,3] doesn't contain 1, so it's valid.
    # Valid: [1,2]? No, contains both.
    # Total: 4 subarrays total - 2 bad = 2 valid. Max gain = 0. Expected: 2
    # Actually [1,2,3] has 3 subarrays: [1],[2],[3],[1,2],[2,3],[1,2,3]
    # Bad: [1,2], [1,2,3] -> 4 valid
    # Hmm, n=3, total subarrays = 3*4/2 = 6. Bad subarrays contain both 1 and 2.
    # These are: [1,2] and [1,2,3]. So 4 valid. Expected: 4
    
    # Edge case: pairs with reversed order
    n5 = 4
    pairs5 = [[3, 2], [4, 1]]
    print("Reversed pairs:", sol.maxSubarrays(n5, pairs5))  # Same as Example 1: 9
    
    # Edge case: n large, no pairs (but constraints say >=1 pair)
    n6 = 3
    pairs6 = [[1, 3]]
    print("Single pair covering 1..3:", sol.maxSubarrays(n6, pairs6))
    # All subarrays containing both 1 and 3: [1,2,3] only
    # Total subarrays = 6, bad = 1, valid = 5
    # Removing the pair gives 6. Expected: 6
    
    # Edge case: pair (1, n)
    n7 = 5
    pairs7 = [[1, 5], [2, 4]]
    print("Pairs [1,5] and [2,4]:", sol.maxSubarrays(n7, pairs7))
    # With both: 
    #   [1,5] blocks any subarray containing both -> only [1,2,3,4,5] is bad
    #   [2,4] blocks any subarray containing both -> [2,3,4] and [1,2,3,4,5]
    # Bad subarrays: [2,3,4], [1,2,3,4,5]
    # Total = 15, bad = 2, valid = 13
    # Remove [1,5]: only [2,4] remains, bad = 2, valid = 13
    # Remove [2,4]: only [1,5] remains, bad = 1, valid = 14
    # Max = 14. Expected: 14