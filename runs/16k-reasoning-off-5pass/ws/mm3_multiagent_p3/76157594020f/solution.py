class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        # Helper function to check if we can achieve max run length <= L
        def feasible(L: int) -> bool:
            ops_left = numOps
            # We'll track the effective value at the previous position (after any flips)
            # and the length of the current run.
            # prev_char: the value of the previous character after potential flips
            # cnt: length of the current run of identical characters
            prev_char = None
            cnt = 0
            
            for c in s:
                # If we have enough ops left, we might flip, but we decide greedily:
                # only flip when the current run would exceed L.
                if c == prev_char:
                    cnt += 1
                else:
                    cnt = 1
                    prev_char = c
                
                if cnt > L:
                    # Need to flip this character to break the run
                    if ops_left <= 0:
                        return False
                    ops_left -= 1
                    # After flipping, this character becomes the opposite,
                    # so it starts a new run of length 1 with the opposite value.
                    prev_char = '1' if c == '0' else '0'
                    cnt = 1
            return True
        
        # Binary search for the minimum L in [1, n]
        low, high = 1, n
        while low < high:
            mid = (low + high) // 2
            if feasible(mid):
                high = mid
            else:
                low = mid + 1
        return low