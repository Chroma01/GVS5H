class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        # Helper function to check if a maximum run length L is feasible
        def is_feasible(L: int) -> bool:
            flips_needed = 0
            i = 0
            while i < n:
                j = i
                # Find the end of the current run of identical characters
                while j < n and s[j] == s[i]:
                    j += 1
                run_length = j - i
                # Calculate flips needed for this run
                flips_needed += (run_length - 1) // L
                i = j
                # Early termination if flips exceed numOps
                if flips_needed > numOps:
                    return False
            return flips_needed <= numOps
        
        # Binary search for the minimum possible maximum run length
        low, high = 1, n
        ans = n
        
        while low <= high:
            mid = (low + high) // 2
            if is_feasible(mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        
        return ans