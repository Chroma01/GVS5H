class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        # Helper function to check if a given max_length L is feasible
        def is_feasible(L: int) -> bool:
            if L <= 0:
                return False
            ops_needed = 0
            # Iterate through the string to find runs of identical characters
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run_length = j - i
                # For a run of length k, flips needed is max(0, (k - 1) // L)
                if run_length > L:
                    ops_needed += (run_length - 1) // L
                i = j
                # Early termination if ops_needed exceeds numOps
                if ops_needed > numOps:
                    return False
            return ops_needed <= numOps
        
        # Binary search for the minimum possible maximum length
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