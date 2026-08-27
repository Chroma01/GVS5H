class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        # Extract run lengths of consecutive identical characters
        runs = []
        current_char = s[0]
        count = 1
        for i in range(1, n):
            if s[i] == current_char:
                count += 1
            else:
                runs.append(count)
                current_char = s[i]
                count = 1
        runs.append(count)
        
        # Helper function: can we make all runs <= L using at most numOps flips?
        def canAchieve(L):
            total_flips = 0
            for run_len in runs:
                # Minimum flips to split a run of length run_len into pieces of size <= L
                total_flips += (run_len + L - 1) // L - 1
                # Early termination for efficiency
                if total_flips > numOps:
                    return False
            return total_flips <= numOps
        
        # Binary search on L (minimum possible longest run length)
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if canAchieve(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo