class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        # Helper function to check if it's possible to achieve max substring length <= k
        def can_achieve(k: int) -> bool:
            flips_needed = 0
            i = 0
            while i < n:
                # Find the length of the current run of identical characters
                j = i
                while j < n and s[j] == s[i]:
                    j += 1
                run_length = j - i
                
                # Calculate flips needed for this run
                # Greedily: skip k characters, then flip the next one, repeat
                count = 0
                pos = 0
                while pos < run_length:
                    pos += k  # skip k characters
                    if pos < run_length:
                        count += 1
                        pos += 1  # skip the flipped character
                flips_needed += count
                
                # Move to the next run
                i = j
                
                # Early termination if already exceeded numOps
                if flips_needed > numOps:
                    return False
            
            return flips_needed <= numOps
        
        # Binary search for the minimum k
        low, high = 1, n
        result = n
        
        while low <= high:
            mid = (low + high) // 2
            if can_achieve(mid):
                result = mid
                high = mid - 1
            else:
                low = mid + 1
        
        return result