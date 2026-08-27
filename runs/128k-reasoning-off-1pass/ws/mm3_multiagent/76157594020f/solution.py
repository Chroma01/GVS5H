class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        # Extract lengths of maximal runs of identical characters
        runs = []
        i = 0
        while i < n:
            j = i
            while j < n and s[j] == s[i]:
                j += 1
            runs.append(j - i)
            i = j
        
        def feasible(L: int) -> bool:
            # Minimum flips needed to ensure every run length <= L
            flips = 0
            for length in runs:
                if length > L:
                    flips += (length - 1) // L
                    if flips > numOps:  # early exit
                        return False
            return flips <= numOps
        
        # Binary search on the answer L in [1, n]
        lo, hi = 1, n
        while lo < hi:
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


# Test harness
if __name__ == "__main__":
    sol = Solution()
    
    # Provided examples
    assert sol.minLength("000001", 1) == 2, f"Example 1 failed: got {sol.minLength('000001', 1)}"
    assert sol.minLength("0000", 2) == 1, f"Example 2 failed: got {sol.minLength('0000', 2)}"
    assert sol.minLength("0101", 0) == 1, f"Example 3 failed: got {sol.minLength('0101', 0)}"
    
    # Additional edge cases
    # Single character
    assert sol.minLength("0", 0) == 1, f"Single 0 no ops failed: got {sol.minLength('0', 0)}"
    assert sol.minLength("1", 5) == 1, f"Single 1 ops failed: got {sol.minLength('1', 5)}"
    
    # All same characters, enough ops to fully alternate
    assert sol.minLength("00000", 4) == 1, f"All zeros full alt failed: got {sol.minLength('00000', 4)}"
    assert sol.minLength("11111", 4) == 1, f"All ones full alt failed: got {sol.minLength('11111', 4)}"
    
    # Alternating already, no ops
    assert sol.minLength("010101", 0) == 1, f"Already alternating failed: got {sol.minLength('010101', 0)}"
    
    # All same, no ops -> answer is n
    assert sol.minLength("00000", 0) == 5, f"All same no ops failed: got {sol.minLength('00000', 0)}"
    assert sol.minLength("11111", 0) == 5, f"All same no ops failed: got {sol.minLength('11111', 0)}"
    
    # Mixed runs, partial ops
    # "0001000" runs: 3, 1, 3. L=1 needs 2+0+2=4 flips, L=2 needs 1+0+1=2 flips
    assert sol.minLength("0001000", 4) == 1, f"Mixed full alt failed: got {sol.minLength('0001000', 4)}"
    assert sol.minLength("0001000", 2) == 2, f"Mixed partial failed: got {sol.minLength('0001000', 2)}"
    assert sol.minLength("0001000", 1) == 3, f"Mixed one op failed: got {sol.minLength('0001000', 1)}"
    assert sol.minLength("0001000", 0) == 3, f"Mixed zero ops failed: got {sol.minLength('0001000', 0)}"
    
    # Merge case: flipping inside a run can merge with adjacent opposite runs
    # s="100001" runs: 1, 4, 1. L=1: (1-1)//1 + (4-1)//1 + (1-1)//1 = 0+3+0 = 3 flips needed
    # But flipping 3 bits in the middle creates three "0"s of length 1 each, 
    # and the surrounding "1"s are already length 1, so total runs become:
    # 1, 1, 1, 1, 1, 1 = all length 1. So L=1 is achievable with 3 ops.
    # The simple formula (len-1)//L correctly handles this case.
    assert sol.minLength("100001", 3) == 1, f"Merge case L=1 failed: got {sol.minLength('100001', 3)}"
    assert sol.minLength("100001", 2) == 2, f"Merge case L=2 failed: got {sol.minLength('100001', 2)}"
    
    # n=1000 stress test
    s_big = "0" * 500 + "1" * 500
    ans = sol.minLength(s_big, 500)
    # With 500 ops on 500 zeros, we can make all runs length 1 -> answer 1
    assert ans == 1, f"Big string failed: got {ans}"
    
    print("All tests passed!")