class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        
        def canAchieve(L: int) -> bool:
            """Check if we can make all runs of identical characters have length <= L
            using at most numOps flips."""
            ops = 0
            # run_len tracks the length of the current run of equal characters
            run_len = 0
            prev_char = None
            for ch in s:
                if ch == prev_char:
                    run_len += 1
                else:
                    run_len = 1
                    prev_char = ch
                
                # If run length would exceed L, flip this character
                if run_len == L + 1:
                    ops += 1
                    run_len = 0  # After flip, current char is opposite, so run resets
                    prev_char = None
            return ops <= numOps
        
        # Binary search on the answer
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if canAchieve(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


# Test with the provided examples
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    assert sol.minLength("000001", 1) == 2, f"Got {sol.minLength('000001', 1)}"
    print("Example 1 passed:", sol.minLength("000001", 1))
    
    # Example 2
    assert sol.minLength("0000", 2) == 1, f"Got {sol.minLength('0000', 2)}"
    print("Example 2 passed:", sol.minLength("0000", 2))
    
    # Example 3
    assert sol.minLength("0101", 0) == 1, f"Got {sol.minLength('0101', 0)}"
    print("Example 3 passed:", sol.minLength("0101', 0)}")
    
    # Additional edge cases
    assert sol.minLength("0", 0) == 1
    assert sol.minLength("1111", 0) == 4
    assert sol.minLength("1111", 3) == 1
    assert sol.minLength("1111", 2) == 2
    assert sol.minLength("000001", 0) == 5
    
    print("All tests passed!")