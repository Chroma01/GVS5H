import math
from typing import List

class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        # Extract lengths of all contiguous runs of identical characters
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
        
        # Binary search for the minimum possible answer
        # The answer is between 1 and n
        left, right = 1, n
        ans = n
        
        while left <= right:
            mid = (left + right) // 2
            ops_needed = 0
            
            # Calculate operations needed to ensure all runs have length <= mid
            for run_len in runs:
                if run_len > mid:
                    # We need to split this run into segments of size at most mid.
                    # Number of segments = ceil(run_len / mid)
                    # Number of flips = segments - 1
                    # Using integer arithmetic: ceil(a/b) = (a + b - 1) // b
                    segments = (run_len + mid - 1) // mid
                    ops_needed += (segments - 1)
            
            if ops_needed <= numOps:
                ans = mid
                right = mid - 1
            else:
                left = mid + 1
                
        return ans