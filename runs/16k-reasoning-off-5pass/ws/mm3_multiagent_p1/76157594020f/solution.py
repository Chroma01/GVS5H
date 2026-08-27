class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        # Helper: compute minimum flips needed to ensure no run exceeds L
        def flips_needed(L: int) -> int:
            total = 0
            i = 0
            while i < n:
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run_len = j - i
                # To split a run of length run_len into pieces of length <= L,
                # we need ceil(run_len / L) - 1 flips (cuts between pieces).
                # If run_len <= L, no flips needed.
                if run_len > L:
                    total += (run_len + L - 1) // L - 1
                i = j
            return total
        
        # Binary search for the smallest L such that flips_needed(L) <= numOps
        lo, hi = 1, n
        answer = n
        while lo <= hi:
            mid = (lo + hi) // 2
            if flips_needed(mid) <= numOps:
                answer = mid
                hi = mid - 1
            else:
                lo = mid + 1
        return answer