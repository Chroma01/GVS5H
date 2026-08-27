from typing import List

class Solution:
    def minOperations(self, queries: List[List[int]]) -> int:
        total_ops = 0
        
        for l, r in queries:
            S = 0
            M = 0
            
            # curr_start represents 4^(k-1)
            curr_start = 1
            k = 1
            
            # Iterate through levels k such that the range [4^(k-1), 4^k - 1] overlaps with [l, r]
            while curr_start <= r:
                # The range for level k is [curr_start, next_start - 1]
                next_start = curr_start * 4
                
                # Calculate intersection of [l, r] and [curr_start, next_start - 1]
                start = max(l, curr_start)
                end = min(r, next_start - 1)
                
                if start <= end:
                    count = end - start + 1
                    S += count * k
                    if k > M:
                        M = k
                
                curr_start = next_start
                k += 1
            
            # The minimum operations is max(ceil(S/2), M)
            # ceil(S/2) can be calculated as (S + 1) // 2 using integer arithmetic
            ops = max((S + 1) // 2, M)
            total_ops += ops
            
        return total_ops