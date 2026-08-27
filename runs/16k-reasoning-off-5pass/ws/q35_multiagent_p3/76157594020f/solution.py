class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        def can_achieve(k: int) -> bool:
            """
            Check if it's possible to make all consecutive identical character 
            substrings have length at most k using at most numOps flips.
            """
            if k <= 0:
                return False
            if k >= n:
                return True
            
            total_flips = 0
            i = 0
            while i < n:
                j = i
                # Find the end of the current block of identical characters
                while j < n and s[j] == s[i]:
                    j += 1
                length = j - i
                # Number of flips needed to break this block into segments of length <= k
                flips_needed = (length - 1) // k
                total_flips += flips_needed
                if total_flips > numOps:
                    return False
                i = j
            return total_flips <= numOps
        
        # Binary search for the minimum k in [1, n]
        low, high = 1, n
        ans = n
        while low <= high:
            mid = (low + high) // 2
            if can_achieve(mid):
                ans = mid
                high = mid - 1
            else:
                low = mid + 1
        return ans