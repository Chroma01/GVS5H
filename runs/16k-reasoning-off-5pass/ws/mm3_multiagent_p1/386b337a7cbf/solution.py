from collections import defaultdict
from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        # even: subsequences of even length (including empty if we had it, but we start empty)
        # odd: subsequences of odd length
        # Each maps sum -> set of valid products (≤ limit)
        even = defaultdict(set)
        odd = defaultdict(set)
        
        for v in nums:
            new_even = defaultdict(set)
            new_odd = defaultdict(set)
            
            # Singleton: subsequence consisting only of v (length 1, odd parity)
            if v <= limit:
                new_odd[v].add(v)
            
            # Process existing even-length subsequences
            for s, p_set in even.items():
                for p in p_set:
                    # Option 1: skip v (keep the subsequence as is)
                    new_even[s].add(p)
                    # Option 2: take v (becomes odd length, adds +v to alternating sum)
                    new_p = p * v
                    if new_p <= limit:
                        new_odd[s + v].add(new_p)
            
            # Process existing odd-length subsequences
            for s, p_set in odd.items():
                for p in p_set:
                    # Option 1: skip v
                    new_odd[s].add(p)
                    # Option 2: take v (becomes even length, adds -v to alternating sum)
                    new_p = p * v
                    if new_p <= limit:
                        new_even[s - v].add(new_p)
            
            even = new_even
            odd = new_odd
        
        ans = -1
        if k in odd:
            ans = max(ans, max(odd[k]))
        if k in even:
            ans = max(ans, max(even[k]))
        return ans