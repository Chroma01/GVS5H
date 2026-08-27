class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        def feasible(L):
            # Check if it's possible to have max block length <= L with <= numOps flips
            flips_needed = 0
            i = 0
            while i < n:
                j = i
                # Find the end of the current block of identical characters
                while j < n and s[j] == s[i]:
                    j += 1
                block_len = j - i
                # Calculate flips needed for this block
                if block_len > L:
                    flips_needed += (block_len - 1) // L
                i = j
                # Early termination if flips exceed numOps
                if flips_needed > numOps:
                    return False
            return flips_needed <= numOps
        
        # Binary search on the answer L
        low, high = 1, n
        while low < high:
            mid = (low + high) // 2
            if feasible(mid):
                high = mid
            else:
                low = mid + 1
        return low