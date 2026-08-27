import math
from typing import List

class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        # Parse the string into run lengths
        runs = []
        current_char = s[0]
        current_len = 1
        for i in range(1, n):
            if s[i] == current_char:
                current_len += 1
            else:
                runs.append(current_len)
                current_char = s[i]
                current_len = 1
        runs.append(current_len)
        
        # Binary search for the minimum length L
        left, right = 1, n
        ans = n
        
        while left <= right:
            mid = (left + right) // 2
            
            # Calculate flips needed for length 'mid'
            flips_needed = 0
            for r in runs:
                # To break a run of length r into segments of max length mid,
                # we need ceil(r / mid) - 1 breaks (flips).
                # ceil(r / mid) is equivalent to (r + mid - 1) // mid using integer division
                segments = (r + mid - 1) // mid
                flips_needed += (segments - 1)
            
            if flips_needed <= numOps:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
                
        return ans