class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        # Precompute the lengths of contiguous segments of identical characters
        segments = []
        if n == 0:
            return 0
        current_char = s[0]
        current_len = 1
        for i in range(1, n):
            if s[i] == current_char:
                current_len += 1
            else:
                segments.append(current_len)
                current_char = s[i]
                current_len = 1
        segments.append(current_len)
        
        # Helper function to check if a given max_len is achievable with numOps
        def can_achieve(max_len: int) -> bool:
            if max_len <= 0:
                return False
            flips_needed = 0
            for seg_len in segments:
                # For a segment of length seg_len, we need floor((seg_len - 1) / max_len) flips
                flips_needed += (seg_len - 1) // max_len
                if flips_needed > numOps:
                    return False
            return flips_needed <= numOps
        
        # Binary search for the smallest max_len in [1, n]
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